from flask_login import current_user
from flask import url_for, redirect, flash, render_template

from database.setup_db.models.base_instance import db
from database.setup_db.models.cars_ml import Cars
from database.setup_db.models.orders_ml import Orders

class CarsHandler:
    def get_brand_model(self):
        brands = db.session.query(Cars.brand).distinct().all()
        brands_lst = [brand[0] for brand in brands]
        
        brand_models = {}
        for b in brands_lst:
            models = db.session.query(Cars.model).filter(Cars.brand == b).distinct().all()
            brand_models[b] = [model[0] for model in models]
        
        return brands_lst, brand_models
    
    def get_cars(self, brand, model=None):
        cars = db.session.query(Cars)
        if brand:
            cars = cars.filter(Cars.brand == brand)
        if model:
            cars = cars.filter(Cars.model == model)
        return cars.all()
    
    def get_car_by_id(self, car_id):
        return db.session.query(Cars).get(car_id)



class OrderCar:
    def order_car(self, car_id):
        if current_user.is_authenticated:
            order = Orders(user_id=current_user.id, car_id=car_id)
            db.session.add(order)
            db.session.commit()
        else:
            flash("Сначала нужно авторизоваться", "error")
        
        return redirect(url_for("car_detail", car_id=car_id))