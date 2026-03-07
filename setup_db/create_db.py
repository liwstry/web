from flask import Flask as _Flask

from setup_db.models.base_instance import db
from setup_db.models.users_ml import Users
from setup_db.models.cars_ml import Cars

def create_db(app: _Flask):
    db.init_app(app)
    with app.app_context():
        db.create_all()