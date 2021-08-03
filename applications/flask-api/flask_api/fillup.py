import logging
from flask import current_app as app, request, jsonify
from flask.views import MethodView
from database.models import Fillup, FillupSerializer, Vehicle
from database import ValidationError

logger = logging.getLogger(__name__)


class ModelNotFound(Exception):
    pass


class FillupView(MethodView):

    def get_vehicle(self, vehicle_id):
        vehicle = app.db.query(Vehicle).filter_by(id=vehicle_id).first()
        if not vehicle:
            raise ModelNotFound
        return vehicle

    def get_fillup(self, vehicle_id, fillup_id):
        fillup = app.db.query(Fillup) \
            .filter_by(vehicle_id=vehicle_id, id=fillup_id) \
            .first()
        if not fillup:
            raise ModelNotFound
        return fillup

    def post(self, vehicle_id):
        try:
            logger.info(f'handling request: {request.json}')
            self.get_vehicle(vehicle_id)
            serializer = FillupSerializer()
            fillup = serializer.load(request.json, session=app.db)
            fillup.vehicle_id = vehicle_id
            app.db.add(fillup)
            app.db.commit()
            prior_fillup = app.db.query(Fillup) \
                .filter(Fillup.vehicle_id == vehicle_id) \
                .filter(Fillup.id != fillup.id) \
                .order_by(Fillup.date.desc(), Fillup.id.desc()) \
                .first()
            if prior_fillup:
                fillup.calculate_mpg(prior_fillup)
            return serializer.dumps(fillup)
        except ModelNotFound:
            return '', 404
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        except Exception:
            return jsonify({'error': 'an unhandled error occurred'}), 500

    def get(self, vehicle_id):
        try:
            self.get_vehicle(vehicle_id)
            serializer = FillupSerializer()
            fillups = app.db.query(Fillup) \
                .filter_by(vehicle_id=vehicle_id) \
                .order_by(Fillup.date.desc(), Fillup.id.desc()) \
                .all()
            for i, fillup in enumerate(fillups):
                if i != len(fillups) - 1:
                    fillup.calculate_mpg(fillups[i+1])
            return serializer.dumps(fillups, many=True)
        except ModelNotFound:
            return '', 404
        except Exception:
            return jsonify({'error': 'an unhandled error occurred'}), 500

    def delete(self, vehicle_id, fillup_id):
        try:
            self.get_vehicle(vehicle_id)
            fillup = self.get_fillup(vehicle_id, fillup_id)
            app.db.delete(fillup)
            app.db.commit()
            return '', 204
        except ModelNotFound:
            return '', 404
        except Exception:
            return jsonify({'error': 'an unhandled error occurred'}), 500
