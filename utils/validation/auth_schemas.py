from flask import flash, render_template
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing import Optional

class SignupSchema(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str
    confirm_password: str
    
    @field_validator("password")
    @classmethod
    def password_validation(cls, v):
        if len(v) < 6:
            flash("Минимальная длина пароля: 6 символов", "error")
        return render_template("signup.html")
    
    @field_validator("confirm_password")
    @classmethod
    def password_match(cls, v, info):
        password = info.data.get("password")
        if password != v:
            flash("Пароли не совпадают", "error")
        return render_template("signup.html")



class SigninSchema(BaseModel):
    email: EmailStr
    password: str