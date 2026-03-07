from setup_db.models.base_instance import db

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    releas = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String, nullable=False)
    type_body = db.Column(db.String, nullable=False)
    transsmission = db.Column(db.String, nullable=False)
    engine_volume = db.Column(db.Float, nullable=False)
    engine_power = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String, nullable=False)