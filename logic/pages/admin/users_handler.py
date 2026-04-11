from flask import request as rq, flash, redirect, url_for, render_template
from flask_login import current_user

from database.setup_db.models.users_ml import Users
from database.setup_db.models.base_instance import db
from utils.check_user import check_user

class UsersHandler:
    def _get_stats(self):
        user_count = Users.query.count()
        admin_count = Users.query.filter_by(is_admin=True).count()
        users = Users.query.all()
        return {
            "user_count": user_count,
            "admin_count": admin_count,
            "users": users
        }
    
    def open_admin(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return render_template("errors/404.html")
        
        return render_template("admin/admin.html", **self._get_stats())
    
    def open_users_panel(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return render_template("errors/404.html")
        
        return render_template("admin/users.html", **self._get_stats())
    
    def create_admin(self):
        email = rq.form.get("email")
        user = check_user(email)
        
        if user:
            if user.is_admin:
                flash("Пользователь уже является администратором", "error")
            else:
                user.is_admin = True
                db.session.commit()
                flash(f"Пользователь: {email} - назначен администратором", "success")
        else:
            flash("Неверный email", "error")
        return redirect(url_for("admin_users"))
    
    def del_admin(self):
        email = rq.form.get("email")
        user = check_user(email)
        
        if user:
            if user.is_admin:
                user.is_admin = False
                db.session.commit()
                flash(f"Права администратора сняты с пользователя: {user.email}", "success")
            else:
                flash("Пользователь не является администратором", "error")
        else:
            flash("Неверный email", "error")
        return redirect(url_for("admin_users"))
    
    
    def switch_admin(self):
        user_id = rq.form.get("user_id")
        user = Users.query.get(user_id)
        if user:
            user.is_admin = not user.is_admin
            db.session.commit()
            if user.is_admin:
                flash(f"Пользователь: {user.email} - назначен администратором", "success")
            else:
                flash(f"Права администратора сняты с пользователя: {user.email}", "success")
        else:
            flash("Пользователь не найден", "error")
        return redirect(url_for("admin_users"))
    
    def del_user(self):
        email = rq.form.get("email")
        user = check_user(email)
        
        if user:
            db.session.delete(user)
            db.session.commit()
            flash(f"Пользователь: {user.email} - удален", "success")
        else:
            flash("Пользователь не найден", "error")
        return redirect(url_for("admin_users"))