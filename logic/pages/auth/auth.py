from flask import request as rq, flash, redirect, url_for, render_template
from flask_login import login_user

from utils.hash_password import create_hash_password, check_hash_password
from database.setup_db.models.users_ml import Users
from database.setup_db.models.base_instance import db
from logs.setup_logs import LogSetup



class Auth:
    def __init__(self):
        self.log = LogSetup(__file__)
    
    def _check_user(self, email):
        return Users.query.filter_by(email=email).first()
    
    def signup(self):
        if rq.method == "POST":
            try:
                name = rq.form.get("name")
                last_name = rq.form.get("last_name")
                email = rq.form.get("email")
                password = rq.form.get("password")
                confirm_password = rq.form.get("confirm_password")
                
                self.log.log("info", "Данные при регистрации получены")
            except Exception as e:
                self.log.log("error", f"Ошибка при получении данных регистрации: {e}")
                flash("Ошибка при получении данных", "error")
                return render_template("signup.html")
            
            if password != confirm_password:
                flash("Пароли не совпадают", "error")
                return render_template("signup.html")
            
            existing_user = self._check_user(email)
            if existing_user:
                flash("Пользователь с таким email уже существует", "error")
                return render_template("signup.html")
            
            try:
                user_add = Users(
                    name=name,
                    last_name=last_name,
                    email=email,
                    password=create_hash_password(password)
                )
                db.session.add(user_add)
                db.session.commit()
                self.log.log("info", f"Пользователь ({email}) зарегистрирован")
            except Exception as e:
                db.session.rollback()
                self.log.log("error", f"Ошибка при регистрации: {e}")
                flash("Ошибка при регистрации", "error")
                return render_template("signup.html")
            
            login_user(user_add)
            
            flash("Успешная регистрация", "success")
            return redirect(url_for("profile"))
        
        return render_template("signup.html")
    
    def signin(self):
        if rq.method == "POST":
            try:
                email = rq.form.get("email")
                password = rq.form.get("password")
                
                self.log.log("info", "Данные для аунтентификации получены")
            except Exception as e:
                self.log.log("error", f"Ошибка получения данных для аунтентификации: {e}")
                flash("Ошибка получения данных")
                return render_template("signin")
            
            user = self._check_user(email)
            
            if user and check_hash_password(password, user.password):
                login_user(user)
                
                self.log.log("info", f"Пользователь ({email}) авторизован")
                flash(f"Здравствуйте, {user.name}", "info")
                return redirect(url_for("profile"))
            else:
                flash("Неверный email или пароль", "error")
                return render_template("signin.html")
        
        return render_template("signin.html")