import requests as rq
import json
from datetime import timedelta, datetime, timezone

from config import Config
from logs.setup_logs import LogSetup

API_KEY = Config.API_TOKEN_WEATHER

log = LogSetup(__file__)

class OpenWeatherAPI:
    def __init__(self):
        self.current_date = (datetime.now(timezone.utc) + timedelta(hours=3))
    
    def check_date_request(self):
        try:
            with open("logic/api/OpenWeatherMap/date_update.json", "r") as file:
                data = json.load(file)
                if self.current_date - datetime.fromisoformat(data["date_request"]) >= timedelta(seconds=7):
                    return True
                return False
        except FileNotFoundError:
            return True
        except Exception as e:
            log.log("error", f"Ошибка при проверке даты запроса: {e}")
            return False
    
    def add_date_request(self):
        data = {"date_request": self.current_date.isoformat()}
        with open("logic/api/OpenWeatherMap/date_update.json", "w") as file:
            json.dump(data, file)

    def get_weather(self, city):
        try:
            # if self.check_date_request():
            #     self.add_date_request()
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = rq.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    temp = data["main"]["temp"]
                    return {
                        "city": city,
                        "temp": temp
                }
            # else:
            #     log.log("warning", "Запрос отменен. Слишком частые запросы")
        except Exception as e:
            log.log("error", f"Ошибка при получении данных погоды для города ({city}): {e}")
            print("Ошибка при получении данных о погоде", e)