from werkzeug.security import generate_password_hash, check_password_hash


def create_hash_password(password):
    return generate_password_hash(password, method="pbkdf2:sha256")

def check_hash_password(password, hashed_password):
    return check_password_hash(hashed_password, password)