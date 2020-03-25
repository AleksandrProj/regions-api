from app.db import db, ma

class Cities(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.parent_id', ondelete="CASCADE"), nullable=True)

class CitiesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cities

    id = ma.auto_field()
    name_city = ma.auto_field(column_name="name")
    region_id = ma.auto_field()