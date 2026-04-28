from flask import request as rq, flash, redirect, url_for, render_template
from flask_login import login_user

import utils.validation as valid
from utils.hash_password import create_hash_password, check_hash_password
from utils.check_user import check_user

from database.setup_db.models.users_ml import Users
from database.setup_db.models.base_instance import db

from logs.setup_logs import LogSetup



class Auth:
    def __init__(self):
        self.log = LogSetup(__file__)
    
    def signup(self):
        if rq.method == "POST":
            try:
                name = rq.form.get("name")
                last_name = rq.form.get("last_name")
                email = rq.form.get("email")
                
                city = rq.form.get("city")
                city = "Москва" if not city else city
                
                password = rq.form.get("password")
                confirm_password = rq.form.get("confirm_password")
                
                
                if not valid.password(password):
                    return render_template("signup.html")
                
                if not valid.email(email):
                    return render_template("signup.html")
                
                if not valid.name(name, last_name):
                    return render_template("signup.html")
                
                if len(city) >= 100:
                    flash("Город не может содержать более 100 символов", "error")
                    return render_template("signup.html")
                
                self.log.log("info", "Данные при регистрации получены")
            except Exception as e:
                self.log.log("error", f"Ошибка при получении данных регистрации: {e}")
                flash("Ошибка при получении данных", "error")
                return render_template("signup.html")
            
            if password != confirm_password:
                flash("Пароли не совпадают", "error")
                return render_template("signup.html")
            
            existing_user = check_user(email)
            if existing_user:
                flash("Пользователь с таким email уже существует", "error")
                return render_template("signup.html")
            
            try:
                user_add = Users(
                    name=name.capitalize(),
                    last_name=last_name.capitalize(),
                    email=email,
                    city=city.capitalize(),
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
            
            user = check_user(email)
            
            if user and check_hash_password(password, user.password):
                login_user(user)
                
                self.log.log("info", f"Пользователь ({email}) авторизован")
                flash(f"Здравствуйте, {user.name}", "info")
                return redirect(url_for("profile"))
            else:
                flash("Неверный email или пароль", "error")
                return render_template("signin.html")
        
        return render_template("signin.html")