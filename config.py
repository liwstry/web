from secrets import token_urlsafe
from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    SECRET_KEY = token_urlsafe(32)
    
    INSTANCE_PATH = "database"
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("EMAIL_ADDRESS")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("EMAIL_ADDRESS")
    API_TOKEN_WEATHER = os.getenv("API_TOKEN_WEATHER")