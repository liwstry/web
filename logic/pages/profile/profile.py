from flask import Flask as _Flask, render_template, redirect, url_for, request as rq, flash
from flask_login import current_user

from database.setup_db.models.base_instance import db
from database.setup_db.models.users_ml import Users

from utils.check_user import check_user
import utils.validation as valid

from logs.setup_logs import LogSetup

class Profile:
    def __init__(self, app: _Flask = None):
        self.app = app
        
        self.log = LogSetup(__file__)
    
    def get_data(self):
        if not current_user.is_authenticated:
            return redirect(url_for("signin"))
        
        user = Users.query.get(current_user.id)
        if not user:
            return redirect(url_for("signin"))
        
        return render_template("profile.html", user=user)
    
    
    def edit_profile(self):
        if not current_user.is_authenticated:
            return redirect(url_for("signin"))
        
        if rq.method != "POST":
            self.get_data()
        
        try:
            name = rq.form.get("first_name")
            last_name = rq.form.get("last_name")
            email = rq.form.get("email")
            city = rq.form.get("city")
            
            if not valid.name(name, last_name):
                return self.get_data()
            
            if not valid.email(email):
                return self.get_data()
            
            if len(city) >= 100:
                flash("Город не может содержать более 100 символов", "error")
                return self.get_data()
            
            self.log.log("info", "Данные для обновления получены")
        except Exception as e:
            self.log.log("error", f"Ошибка при получении данных: {e}")
            flash("Ошибка при получении данных", "error")
            return self.get_data()
        
        if email != current_user.email and check_user(email):
            flash("Email занят", "error")
            return self.get_data()
        
        if not name or not last_name or not email or not city:
            flash("Вы оставили поле пустым", "error")
            return self.get_data()
        
        if (
            name == current_user.name and last_name == current_user.last_name
            and email == current_user.email and city == current_user.city
            ):
            flash("Вы не изменили данные", "error")
            return self.get_data()
        
        try:
            current_user.name = name
            current_user.last_name = last_name
            current_user.email = email
            current_user.city = city
            
            db.session.commit()
            self.log.log("info", f"Данные пользователя ({email}) обновлены")
        except Exception as e:
            self.log.log("error", f"Ошибка при обновлении данных: {e}")
            flash("Ошибка при обновлении данных", "error")
            return self.get_data()
        
        flash("Профиль обновлен", "success")
        return redirect(url_for("profile"))