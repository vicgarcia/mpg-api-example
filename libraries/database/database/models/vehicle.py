import sqlalchemy as sa
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from datetime import datetime
from .base import Base
from .fillup import Fillup


class Vehicle(Base):
    __tablename__ = 'vehicle'

    id = sa.Column(sa.Integer(), primary_key=True)
    year = sa.Column(sa.Integer(), nullable=False)
    make = sa.Column(sa.String(40), nullable=False)
    model = sa.Column(sa.String(40), nullable=False)
    vin = sa.Column(sa.String(40), nullable=False)
    created = sa.Column(sa.DateTime(), default=datetime.utcnow)
    fillups = relationship(Fillup)


class VehicleSerializer(SQLAlchemyAutoSchema):

    created = auto_field(dump_only=True)

    class Meta:
        model = Vehicle
        load_instance = True
        # explicitly provide fields to control ordering along with ordered = True
        fields = ('id', 'year', 'vin', 'make', 'model', 'created')
        ordered = True

