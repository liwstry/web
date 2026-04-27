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
from logic.pages.cars.cars import OrderCar
from logic.pages.cars.cars import CarsHandler

from logic.services.change_password.change_password import ChangePassword

class Routes:
    def __init__(self, app: _Flask, socketio: _SocketIO, mail: _Mail, token: _URLSafeTimedSerializer):
        self.app = app
        
        self.socketio = socketio
        self.mail = mail
        self.token = token
        
        self.auth = Auth()
        self.profile_handler = Profile()
        self.admin = UsersHandler()
        self.cars = CarsHandler()
        self.order_car = OrderCar()
        self.change_password = ChangePassword(app, mail, token)
        self.add_car = AddCars()
        
        self.lst_inst = (self.app, self.socketio, self.mail, self.token)
        
    def _transfer_parameters(self, *classes):
        for cls in classes:
            cls(*self.lst_inst).run_routes()
        
    def run_routes(self):
        from routes.auth_routes import AuthRoutes
        from routes.admin_routes import AdminRoutes
        from routes.cars_routes import CarsRoutes
        from routes.profile_routes import ProfileRoutes
        from routes.change_password_routes import ChangePasswordRoutes
        
        self._transfer_parameters(AuthRoutes, AdminRoutes, CarsRoutes, ProfileRoutes, ChangePasswordRoutes)
        
        @self.app.route("/")
        def index():
            return render_template("index.html")
        
        @self.app.route("/logout")
        def logout():
            logout_user()
            flash("Вы вышли из аккаунта", "warning")
            return redirect(url_for("index"))