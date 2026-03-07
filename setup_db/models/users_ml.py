from sqlalchemy import func

from setup_db.models.base_instance import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    date_create = db.Column(db.DateTime, default=func.datetime(func.now(), "+3 hours"), index=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)