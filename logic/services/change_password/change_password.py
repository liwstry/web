from flask import request as rq, flash, redirect, url_for, render_template
from flask_login import current_user
from itsdangerous import SignatureExpired

# Для аннотации
from flask import Flask as _Flask
from flask_mail import Mail as _Mail
from itsdangerous import URLSafeTimedSerializer as _URLSafeTimedSerializer
###############

from logic.services.email.send_to_email import send_to_email
from logs.setup_logs import LogSetup
from database.setup_db.models.base_instance import db
from database.setup_db.models.users_ml import Users
from utils.hash_password import create_hash_password

class ChangePassword:
    def __init__(self, app: _Flask, mail: _Mail, gen_token: _URLSafeTimedSerializer):
        self.app = app
        self.mail = mail
        self.gen_token = gen_token
        
        self.log = LogSetup(__file__)
    
    def gen_url_token(self):
        if not current_user.is_authenticated:
            flash("Вы не авторизованы", "error")
            return redirect(url_for("signin"))
        
        try:
            token = self.gen_token.dumps(current_user.id, salt="change_password")
            url = url_for("change_password", token=token, _external=True)
            html = render_template("email/links/change_password_link.html", username=current_user.name, url=url)
            msg = f"Ссылка для смены пароля: {url}"
            
            send_to_email(self.mail, subject="Смена пароля", sender=self.app.config["MAIL_DEFAULT_SENDER"], recipients=[current_user.email], text_msg=msg, html_body=html)
            
            self.log.log("info", f"Ссылка для смены пароля отправлена на ({current_user.email})")
            flash("Ссылка для смены пароля отправлена на почту", "success")
        except Exception as e:
            self.log.log("error", f"Ошибка при отправке ссылки для смены пароля: {e}")
            flash("Ошибка. Сообщение не отправлено", "error")
            
        return redirect(url_for("profile"))
    
    def change_password(self, token):
        try:
            user_id = self.gen_token.loads(token, salt="change_password", max_age=3600)
        except SignatureExpired:
            self.log.log("debug", "Ссылка для смены пароля просрочена")
            flash("Ссылка для смены пароля просрочена", "error")
            return redirect(url_for("signin"))
        except Exception as e:
            self.log.log("error", f"Ошибка при проверке ссылки для смены пароля: {e}")
            flash("Ссылка для смены пароля не действительна", "error")
            return redirect(url_for("signin"))
        
        user = Users.query.get(user_id)
        if not user: 
            self.log.log("debug", "Пользователь не найден")
            flash("Пользователь не найден", "error")
            return redirect(url_for("signin"))
        
        if rq.method == "POST":
            new_password = rq.form.get("password")
            confirm_password = rq.form.get("confirm_password")
            
            if new_password != confirm_password:
                flash("Пароли не совпадают", "error")
                return render_template("email/forms/change_password.html", username=user.email, token=token)
            
            hash_password = create_hash_password(new_password)
            user.password = hash_password
            
            try:
                db.session.commit()
                self.log.log("info", f"Пароль пользователя ({user.email}) изменен")
                flash("Пароль успешно изменен", "success")
                return redirect(url_for("signin"))
            except Exception as e:
                self.log.log("error", f"Ошибка при изменении пароля: {e}")
                flash("Ошибка при изменении пароля", "error")
                
        return render_template("email/forms/change_password.html", username=user.email, token=token)