from flask import Flask as _Flask
from flask_socketio import SocketIO as _SocketIO
from flask_mail import Mail as _Mail
from itsdangerous import URLSafeTimedSerializer as _URLSafeTimedSerializer



from flask import render_template, request as rq, flash, redirect, url_for
from flask_login import logout_user

from logic.pages.auth.auth import Auth
from logic.pages.profile.profile import Profile
from logic.pages.admin.users_handler import UsersHandler
from logic.pages.admin.add_cars import AddCars
from logic.pages.cars.cars import CarsHandler

from logic.services.change_password.change_password import ChangePassword

class Routes:
    def __init__(self, app: _Flask, socketio: _SocketIO, mail: _Mail, token: _URLSafeTimedSerializer):
        self.app = app
        
        self.socketio = socketio
        self.mail = mail
        self.token = token
        self.lst_inst = [self.app, self.socketio, self.mail, self.token]
        
        self.auth = Auth()
        self.profile_handler = Profile()
        self.admin = UsersHandler()
        self.cars = CarsHandler()
        self.change_password = ChangePassword(app, mail, token)
        self.add_car = AddCars()
        
    def run_routes(self):
        
        from routes.auth_routes import AuthRoutes
        AuthRoutes(*self.lst_inst).run_routes()
        
        from routes.admin_routes import AdminRoutes
        AdminRoutes(*self.lst_inst).run_routes()
        
        @self.app.route("/")
        def index():
            return render_template("index.html")
        
        
        @self.app.route("/profile", methods=["get", "post"])
        def profile():
            if rq.method == "POST":
                return self.profile_handler.edit_profile()
            return self.profile_handler.get_data()
        
        @self.app.route("/change-password", methods=["post"])
        def change_password_link():
            return self.change_password.gen_url_token()
        
        @self.app.route("/change-password/<token>", methods=["get", "post"])
        def change_password(token):
            return self.change_password.change_password(token)
        
        @self.app.route("/logout")
        def logout():
            logout_user()
            flash("Вы вышли из аккаунта", "warning")
            return redirect(url_for("index"))
        
        
        
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
            cars = []
            
            if brand and model:
                cars = self.cars.get_cars(brand, model)
                return render_template("card_cars.html", cars=cars, brand=brand, model=model)
        
        @self.app.route("/cars/<car_id>")
        def car_detail(car_id):
            car = self.cars.get_car_by_id(car_id)
            if not car:
                flash("Автомобиль не найден", "warning")
                return redirect(url_for("cars_brands"))
            return render_template("car_detail.html", car=car)