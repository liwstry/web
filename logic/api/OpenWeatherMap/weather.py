import requests as rq
import json
from datetime import timedelta, datetime, timezone

from config import Config
from logs.setup_logs import LogSetup

API_KEY = Config.API_TOKEN_WEATHER

log = LogSetup(__file__)

class OpenWeatherAPI:
    def __init__(self, city):
        self.city = city
        
        self.current_date = (datetime.now(timezone.utc) + timedelta(hours=3))
    
    def check_date_request(self):
        try:
            with open("logic/api/OpenWeatherMap/date_update.json", "r") as file:
                date_request = json.load(file)["date_request"]
                if self.current_date - datetime.fromisoformat(date_request) >= timedelta(seconds=7):
                    return True
                print("ЧАСТЫЙ ЗАПРОС")
                return False
        except FileNotFoundError:
            return True
        except Exception as e:
            log.log("error", f"Ошибка при проверке даты запроса: {e}")
            return False
    
    def record_data(self, temp):
        data = {
                "date_request": self.current_date.isoformat(),
                "temp": temp
                }
        with open("logic/api/OpenWeatherMap/data_response.json", "w") as file:
            json.dump(data, file, indent=4)

    def response_data(self):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={API_KEY}&units=metric"
            response = rq.get(url)
            
            if response.status_code == 200:
                data = response.json()
                self.record_data(data["main"]["temp"])
        except Exception as e:
            log.log("error", f"Ошибка при получении данных погоды для города ({self.city}): {e}")
            print("Ошибка при получении данных о погоде", e)
    
    def get_weather(self):
        temp = 0
        
        if not self.check_date_request:
            with open("logic/api/OpenWeatherMap/data_response.json", "r") as file:
                temp = json.load(file)
                return {
                    "city": self.city,
                    "temp": temp
                }
        
        self.response_data()
        with open("logic/api/OpenWeatherMap/data_response.json", "r") as file:
            temp = json.load(file)["temp"]
        
        return {
            "city": self.city,
            "temp": temp
        }