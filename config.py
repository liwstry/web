from secrets import token_urlsafe

class Config():
    SECRET_KEY = token_urlsafe(32)
    
    INSTANCE_PATH = "database"
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


