from database.setup_db.models.users_ml import Users

def check_user(email):
        return Users.query.filter_by(email=email).first()