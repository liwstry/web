from flask import Flask
from flask_login import LoginManager

from routes import Routes
from config import Config
from setup_db.create_db import create_db
from setup_db.models.users_ml import Users
from logs.setup_logs import LogSetup

log = LogSetup(__file__)

log.log("info", "Инициализация основных компонентов приложения")

try:
    app = Flask(__name__)
    app.config.from_object(Config())
    
    lm = LoginManager()
    lm.init_app(app)
    
    app.instance_path = Config.INSTANCE_PATH
    create_db(app)
    
    routes = Routes(app)
    routes.run_routes()

except Exception as e:
    log.log("critical", f"Ошибка инициализации компонента: {e}")
    log.log("info", "Запуск остановлен")
    print(e)
    exit(1)

@lm.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

if __name__ == "__main__":
    log.log("info", "Приложение запущено")
    try:
        app.run(debug=True)
        
    except Exception as e:
        log.log("critical", f"Ошибка при работе приложения: {e}")
        print(e)
        exit(1)
    finally:
        log.log("info", "Приложение остановлено")