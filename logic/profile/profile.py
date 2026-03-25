from flask import Flask as _Flask, render_template, redirect, url_for, request as rq, flash
from flask_login import current_user

from setup_db.models.base_instance import db
from setup_db.models.users_ml import Users
from utils.check_user import check_user
from logs.setup_logs import LogSetup

log = LogSetup(__file__)

class Profile:
    def __init__(self, app: _Flask = None):
        self.app = app
    
    def get_data(self):
        if not current_user.is_authenticated:
            return redirect(url_for("signin"))
        
        user = Users.query.get(current_user.id)
        if not user:
            return redirect(url_for("signin"))
        
        return render_template("profile.html", user=user)
    
    
    def edit_profile(self):
        if rq.method != "POST":
            self.get_data()
        
        try:
            name = rq.form.get("first_name")
            last_name = rq.form.get("last_name")
            email = rq.form.get("email")
        except Exception as e:
            log.log("error", e)
            flash("Ошибка", "danger")
            return self.get_data()
        
        if email != current_user.email and check_user(email):
            flash("Email занят")
            return self.get_data()
        
        if not name or not last_name or not email:
            flash("Вы оставили поле пустым", "warning")
            return self.get_data()
        
        if name == current_user.name and last_name == current_user.last_name and email == current_user.email:
            flash("Вы не изменили данные", "warning")
            return self.get_data()
        
        # TODO исправить обновление не нужных данных
        current_user.name = name
        current_user.last_name = last_name
        current_user.email = email
        
        db.session.commit()
        
        flash("Профиль обновлен", "success")
        return redirect(url_for("profile"))
    