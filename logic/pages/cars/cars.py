from database.setup_db.models.base_instance import db
from database.setup_db.models.cars_ml import Cars

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