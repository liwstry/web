from flask import request as rq, redirect, url_for, render_template, flash

from routes.routes_init import Routes

class CarsRoutes(Routes):
    def run_routes(self):
        @self.app.route("/cars_brands", methods=["get", "post"])
        def cars_brands():
            brands, brand_models = self.cars.get_brand_model()
            selected_brand = None
            selected_model = None
            
            if rq.method == "POST":
                brand = rq.form.get("brand")
                model = rq.form.get("model")
                
                selected_brand = brand
                selected_model = model
                
                if brand and model:
                    return redirect(url_for("cars_list", brand=brand, model=model))
            
            return render_template(
                "cars_brands.html",
                brands=brands,
                brand_models=brand_models,
                selected_brand=selected_brand,
                selected_model=selected_model
            )
        
        @self.app.route("/cars_list")
        def cars_list():
            brand = rq.args.get("brand")
            model = rq.args.get("model")
            cars = self.cars.get_cars(brand, model)
            
            return render_template("card_cars.html", cars=cars, brand=brand, model=model)
        
        @self.app.route("/cars/<car_id>")
        def car_detail(car_id):
            car = self.cars.get_car_by_id(car_id)
            if not car:
                flash("Автомобиль не найден", "warning")
                return redirect(url_for("cars_brands"))
            return render_template("car_detail.html", car=car)
        
        @self.app.route("/cars/order/<car_id>", methods=["post"])
        def order_car(car_id):
            return self.order_car.order_car(car_id)