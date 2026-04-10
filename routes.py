from flask import render_template, request as rq, flash, redirect, url_for
# from flask_socketio import emit
from flask_login import logout_user

from flask import Flask as _Flask
from flask_socketio import SocketIO as _SocketIO
from flask_mail import Mail as _Mail
from itsdangerous import URLSafeTimedSerializer as _URLSafeTimedSerializer

from logic.pages.auth.auth import Auth
from logic.pages.profile.profile import Profile
from logic.pages.admin.users_handler import UsersHandler
from logic.services.change_password.change_password import ChangePassword

class Routes:
    def __init__(self, app: _Flask, socketio: _SocketIO, mail: _Mail, token: _URLSafeTimedSerializer):
        self.app = app
        
        self.auth = Auth()
        self.profile_handler = Profile()
        self.admin = UsersHandler()
        self.change_password = ChangePassword(app, mail, token)
        
    def run_routes(self):
        
        @self.app.route("/")
        def index():
            return render_template("index.html")
        
        
        
        @self.app.route("/signin", methods=["get", "post"])
        def signin():
            if rq.method == "POST":
                return self.auth.signin()
            return render_template("signin.html")
        
        @self.app.route("/signup", methods=["get", "post"])
        def signup():
            if rq.method == "POST":
                return self.auth.signup()
            return render_template("signup.html")
        
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
        
        
        
        @self.app.route("/cars_brands")
        def cars_brand():
            return render_template("cars_brands.html")
        
        @self.app.route("/cars_models")
        def cars_model():
            return render_template("cars_model.html")
        
        
        @self.app.route("/admin")
        def admin():
            return self.admin.open_admin()
        
        @self.app.route("/admin/server")
        def server():
            return render_template("admin/server.html")
        
        @self.app.route("/admin/users")
        def admin_users():
            return self.admin.open_users_panel()
        
        @self.app.route("/admin/users/admin-add", methods=["POST"])
        def admin_add():
            return self.admin.create_admin()
        
        @self.app.route("/admin/users/admin-remove", methods=["post"])
        def admin_remove():
            return self.admin.del_admin()
        
        @self.app.route("/admin/users/admin-switch", methods=["post"])
        def admin_switch():
            return self.admin.switch_admin()
        
        @self.app.route("/admin/users/user-remove", methods=["post"])
        def user_remove():
            return self.admin.del_user()