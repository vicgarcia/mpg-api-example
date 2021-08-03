import logging
from flask import current_app as app, request, jsonify
from flask.views import MethodView
from database.models import Vehicle, VehicleSerializer
from database import ValidationError

logger = logging.getLogger(__name__)


class VehicleNotFound(Exception):
    pass


class VehicleView(MethodView):

    def get_vehicle(self, vehicle_id):
        vehicle = app.db.query(Vehicle).filter_by(id=vehicle_id).first()
        if not vehicle:
            raise VehicleNotFound
        return vehicle

    def post(self):
        try:
            logger.info(f'handling request: {request.json}')
            serializer = VehicleSerializer()
            vehicle = serializer.load(request.json, session=app.db)
            app.db.add(vehicle)
            app.db.commit()
            return serializer.dumps(vehicle)
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        except Exception as e:
            return jsonify({'error': 'an unhandled error occurred'}), 500

    def _get_single(self, vehicle_id):
        try:
            serializer = VehicleSerializer()
            vehicle = self.get_vehicle(vehicle_id)
            return serializer.dumps(vehicle)
        except VehicleNotFound as e:
            return '', 404
        except Exception as e:
            return jsonify({'error': 'an unhandled error occurred'}), 500

    def _get_multiple(self):
        try:
            serializer = VehicleSerializer()
            vehicles = app.db.query(Vehicle).all()
            return serializer.dumps(vehicles, many=True)
        except Exception as e:
            return jsonify({'error': 'an unhandled error occurred'}), 500

    def get(self, vehicle_id):

        if vehicle_id is not None:
            return self._get_single(vehicle_id)
        else:
            return self._get_multiple()

    def patch(self, vehicle_id):
        try:
            logger.info(f'handling request: {request.json}')
            serializer = VehicleSerializer()
            vehicle = self.get_vehicle(vehicle_id)
            vehicle = serializer.load(request.json, session=app.db, instance=vehicle, partial=True)
            app.db.add(vehicle)
            app.db.commit()
            return serializer.dumps(vehicle)
        except VehicleNotFound as e:
            return '', 404
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        except Exception as e:
            return jsonify({'error': 'an unhandled error occurred'}), 500

    def delete(self, vehicle_id):
        try:
            vehicle = self.get_vehicle(vehicle_id)
            app.db.delete(vehicle)
            app.db.commit()
            return '', 204
        except VehicleNotFound as e:
            return '', 404
        except Exception as e:
            return jsonify({'error': 'an unhandled error occurred'}), 500
