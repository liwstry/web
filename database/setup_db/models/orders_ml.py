from sqlalchemy import func
from database.setup_db.models.base_instance import db

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"), nullable=False)
    order_date = db.Column(db.DateTime, default=func.datetime(func.now(), "+3 hours"), index=True)