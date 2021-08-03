import logging
from flask import Flask, _app_ctx_stack
from database import scoped_session, SessionLocal
from .rest import GET, POST, PATCH, DELETE
from .vehicle import VehicleView
from .fillup import FillupView

logger = logging.getLogger(__name__)


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    app.db = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

    vehicle_view = VehicleView.as_view('vehicles')
    app.add_url_rule('/vehicles/', view_func=vehicle_view, methods=[GET], defaults={'vehicle_id': None})
    app.add_url_rule('/vehicles/', view_func=vehicle_view, methods=[POST])
    app.add_url_rule('/vehicles/<int:vehicle_id>/', view_func=vehicle_view, methods=[GET, PATCH, DELETE])
    logger.info('loaded vehicle urls')

    # example with the RestApiView abstract
    # from .rest import VehicleView
    # VehicleView.add_url_rules(app, '/vehicles/', 'vehicles')

    fillup_view = FillupView.as_view('fillups')
    app.add_url_rule('/vehicles/<int:vehicle_id>/fillups/', view_func=fillup_view, methods=[GET, POST])
    app.add_url_rule('/vehicles/<int:vehicle_id>/fillups/<int:fillup_id>/', view_func=fillup_view, methods=[DELETE])

    return app
