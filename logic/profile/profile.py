from flask import render_template, redirect, url_for
from flask_login import current_user

from setup_db.models.users_ml import Users

class Profile:
    def __init__(self):
        pass
    
    def get_data(self):
        if not current_user.is_authenticated:
            return redirect(url_for("signin"))
        
        user = Users.query.get(current_user.id)
        if not user:
            return redirect(url_for("signin"))
        
        return render_template("profile.html", user=user)