from flask_socketio import SocketIO as _SocketIO

import time

from logic.api.OpenWeatherMap.weather import OpenWeatherAPI

class WeatherSocket:
    def __init__(self, socketio: _SocketIO):
        self.socketio = socketio
        self.weather = OpenWeatherAPI()

    def run_weather_socket(self):
        @self.socketio.on("get_weather")
        def weather():
            self.socketio.emit("weather_update", self.weather.get_weather("Москва"))

    def _weather_update(self):
        while True:
            self.socketio.emit("weather_update", self.weather.get_weather("Москва"))
            time.sleep(60)
    
    def run(self):
        self.run_weather_socket()
        self.socketio.start_background_task(target=self._weather_update)