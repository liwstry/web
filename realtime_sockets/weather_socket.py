from flask_socketio import SocketIO as _SocketIO

from logic.api.OpenWeatherMap.weather import OpenWeatherAPI

class WeatherSocket:
    def __init__(self, socketio: _SocketIO):
        self.socketio = socketio
        self.weather = OpenWeatherAPI()

    def run_weather_socket(self):
        @self.socketio.on("get_weather")
        def weather():
            self.socketio.emit("weather_update", self.weather.get_weather())
    
    def run(self):
        self.run_weather_socket()