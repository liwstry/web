from flask import Flask
from flask_login import LoginManager

from routes import Routes
from config import Config
from setup_db.create_db import create_db
from setup_db.models.users_ml import Users

app = Flask(__name__)
app.config.from_object(Config())

lm = LoginManager()
lm.init_app(app)

app.instance_path = Config.INSTANCE_PATH
create_db(app)

routes = Routes(app)
routes.run_routes()

@lm.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

if __name__ == "__main__":
    app.run(debug=True)