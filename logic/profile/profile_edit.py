from flask import request as rq, redirect, url_for, flash
from flask_login import current_user

def edit_profile():
    try:
        if rq.method == "POST":
            current_user.name = rq.form.get("first_name")
            current_user.last_name = rq.form.get("last_name")
            current_user.email = rq.form.get("email")
            
            flash("Профиль обновлен", "success")
            return redirect(url_for("profile"))
    except Exception as e:
        flash("Не удалось обновить профиль", "danger")
        return redirect(url_for("profile"))