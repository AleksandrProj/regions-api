from app.db import db, ma
from app.cities.models import CitiesSchema

class Regions(db.Model):
    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False, unique=True)
    cities = db.relationship('Cities', backref=db.backref('region', cascade="all, delete"), lazy=True)

class RegionsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Regions

    id = ma.auto_field()
    name_region = ma.auto_field(column_name="name")
    region_id = ma.auto_field(column_name="parent_id")
    cities = ma.Nested(CitiesSchema, many=True)
