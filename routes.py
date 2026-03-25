from flask import Flask as _Flask, render_template, request as rq, flash, redirect, url_for
from flask_login import logout_user

from logic.auth.auth import Auth
from logic.profile.profile import Profile
from logic.admin.users_handler import UsersHandler

class Routes:
    def __init__(self, app: _Flask):
        self.app = app
        
        self.auth = Auth()
        self.profile_handler = Profile()
        self.admin = UsersHandler()
        
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
            return render_template("admin/admin.html")
        
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