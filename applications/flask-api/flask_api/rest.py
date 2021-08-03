import logging
from flask import current_app, json, request, jsonify
from flask.views import MethodView
from database import ValidationError

logger = logging.getLogger(__name__)


GET = 'GET'
POST = 'POST'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'


class NotFoundException(Exception):
    pass


class RestApiView(MethodView):
    model_class = None
    serializer_class = None

    def get_object(self, obj_id):
        obj = current_app.db.query(self.model_class).filter_by(id=obj_id).first()
        if not obj:
            raise NotFoundException
        return obj

    def post(self):
        try:
            serializer = self.serializer_class()
            obj = serializer.load(request.json, session=current_app.db)
            current_app.db.add(obj)
            current_app.db.commit()
            return serializer.dumps(obj)
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        except Exception as e:
            return jsonify({'error': 'an unhandled error occurred'}), 500

    def get(self, obj_id):
        try:
            serializer = self.serializer_class()
            if obj_id is not None:
                obj = self.get_object(obj_id)
                return serializer.dumps(obj)
            else:
                objs = current_app.db.query(self.model_class).all()
                return serializer.dumps(objs, many=True)
        except NotFoundException:
            return '', 404
        except Exception as e:
            return jsonify({'error': 'an unhandled error occurred'}), 500

    def patch(self, obj_id):
        try:
            serializer = self.serializer_class()
            obj = self.get_object(obj_id)
            obj = serializer.load(request.json, session=current_app.db, instance=obj, partial=True)
            current_app.db.add(obj)
            current_app.db.commit()
            return serializer.dumps(obj)
        except NotFoundException:
            return '', 404
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400
        except Exception as e:
            return jsonify({'error': 'an unhandled error occurred'}), 500

    def delete(self, obj_id):
        try:
            obj = self.get_object(obj_id)
            current_app.db.delete(obj)
            current_app.db.commit()
            return '', 204
        except NotFoundException:
            return '', 404
        except Exception as e:
            return jsonify({'error': 'an unhandled error occurred'}), 500

    @classmethod
    def add_url_rules(cls, app, base_url, view_name):
        as_view = cls.as_view(view_name)
        app.add_url_rule(f"{base_url}", view_func=as_view, methods=[GET], defaults={'obj_id': None})
        app.add_url_rule(f"{base_url}", view_func=as_view, methods=[POST])
        app.add_url_rule(f"{base_url}/<int:obj_id>", view_func=as_view, methods=[GET, PATCH, DELETE])



from database.models import Vehicle, VehicleSerializer

class VehicleView(RestApiView):
    model_class = Vehicle
    serializer_class = VehicleSerializer
