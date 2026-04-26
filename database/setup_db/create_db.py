from flask import Flask as _Flask

from database.setup_db.models.base_instance import db
from database.setup_db.models.users_ml import Users
from database.setup_db.models.cars_ml import Cars
from database.setup_db.models.orders_ml import Orders
from logs.setup_logs import LogSetup

log = LogSetup(__file__)

def create_db(app: _Flask):
    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
            log.log("info", "База данных создана")
    except Exception as e:
        log.log("error", e)
        raise e