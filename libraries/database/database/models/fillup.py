import sqlalchemy as sa
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields
from datetime import datetime
from .base import Base


class Fillup(Base):
    __tablename__ = 'fillup'

    id = sa.Column(sa.Integer(), primary_key=True)
    date = sa.Column(sa.Date(), nullable=False)
    mileage = sa.Column(sa.Integer(), nullable=False)
    gallons = sa.Column(sa.Float(), nullable=False)
    vehicle_id = sa.Column(sa.Integer(), sa.ForeignKey('vehicle.id'))

    mpg = None

    def calculate_mpg(self, prior_fillup):
        mpg = (self.mileage - prior_fillup.mileage) / self.gallons
        self.mpg = round(mpg, 1)


class FillupSerializer(SQLAlchemyAutoSchema):

    mpg = fields.Float(dump_only=True)

    class Meta:
        model = Fillup
        load_instance = True
        fields = ('id', 'date', 'mileage', 'gallons', 'mpg')
        ordered = True
