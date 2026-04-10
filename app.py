from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

from routes import Routes
from config import Config
from setup_db.create_db import create_db
from setup_db.models.users_ml import Users
from logs.setup_logs import LogSetup
from realtime_sockets.server_socket import ServerSocket
from realtime_sockets.weather_socket import WeatherSocket

log = LogSetup(__file__)

log.log("info", "Инициализация основных компонентов приложения")

try:
    app = Flask(__name__)
    app.config.from_object(Config())
    socketio = SocketIO(app)
    
    lm = LoginManager()
    lm.init_app(app)
    
    app.instance_path = Config.INSTANCE_PATH
    create_db(app)
    
    mail = Mail(app)
    token = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    
    routes = Routes(app, socketio, mail, token)
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
    server = ServerSocket(socketio)
    weather = WeatherSocket(socketio)
    
    weather.run()
    server.run()
    
    
    log.log("info", "Приложение запущено")
    
    try:
        socketio.run(app, debug=True)
    
    except Exception as e:
        log.log("critical", f"Ошибка при работе приложения: {e}")
        print(e)
        exit(1)
    finally:
        log.log("info", "Приложение остановлено")