from flask import flash

import re

from email_validator import validate_email, EmailNotValidError
from eng_to_ru import Translator

from logs.setup_logs import LogSetup

log = LogSetup(__name__)

def password(password):
    if len(password) == 0 or password is None or password == "" or password.isspace():
        flash("Пароль не может быть пустым", "error")
        return False
    
    if len(password) > 100:
        flash("Пароль не может содержать более 100 символов", "error")
        return False
    
    if re.search(r"[а-яА-Я]+", password):
        flash("Пароль не может содержать кириллицу", "error")
        return False
    
    if len(password) < 6:
        flash("Пароль должен содержать более 6 символов", "error")
        return False
    
    if not re.search(r"\d+", password):
        flash("Пароль должен содержать хотябы одну цифру", "error")
        return False
    
    if not re.search(r"[A-Z]+", password):
        flash("Пароль должен содержать хотябы одну заглавную букву", "error")
        return False
    
    if not re.search(r"[a-z]+", password):
        flash("Пароль должен содержать хотябы одну строчную букву", "error")
        return False
    
    return True

def email(email):
    if not email or len(email) == 0 or email is None or email == "" or email.isspace():
        flash("Почта не может быть пустой", "error")
        return False
    
    if len(email) > 100:
        flash("Почта не может содержать более 100 символов", "error")
        return False
    
    try:
        validate_email(email)
    except EmailNotValidError as e:
        translator = Translator()
        try:
            translat_text = translator.run(str(e))
        except Exception as e:
            log.log("error", f"Ошибка при переводе текста: {e}")
            translat_text = None
        
        err_text = "Некорректный адрес электронной почты" if translat_text is None else translat_text
        
        flash(err_text, "error")
        return False
    
    return True

def name(name, last_name):
    if (
        len(name) == 0 or len(last_name) == 0 or name is None
        or name == "" or last_name == "" or last_name is None or name.isspace() or last_name.isspace()
        ):
        flash("Имя/Фамилия не может быть пустым", "error")
        return False

    if len(name) > 100 or len(last_name) > 100:
        flash("Имя/Фамилия не может содержать более 100 символов", "error")
        return False

    if re.search(r"[0-9]+", name):
        flash("Имя/Фамилия не может содержать цифры", "error")
        return False
    
    return True