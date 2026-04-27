import requests as rq
import json
from datetime import timedelta, datetime, timezone

from config import Config
from logs.setup_logs import LogSetup

log = LogSetup(__file__)

API_KEY = Config.API_TOKEN_WEATHER

class OpenWeatherAPI:
    def __init__(self, city):
        self.city = city

    @property
    def current_date(self):
        return datetime.now(timezone.utc) + timedelta(hours=3)

    def check_date_request(self):
        try:
            with open("logic/api/OpenWeatherMap/data_response.json", "r") as file:
                date_request = json.load(file)["date_request"]
                last_request = datetime.fromisoformat(date_request)
                time_passed = self.current_date - last_request
                if time_passed >= timedelta(minutes=1):
                    return True
                
                log.log("info", f"Частый запрос для города {self.city}. Прошло {time_passed.total_seconds():.1f}")
                return False
        except FileNotFoundError:
            return True
        except Exception as e:
            log.log("error", f"Ошибка при проверке даты запроса: {e}")
            return False

    def _record_data(self, temp):
        data = {
            "date_request": self.current_date.isoformat(),
            "temp": temp
        }
        with open("logic/api/OpenWeatherMap/data_response.json", "w") as file:
            json.dump(data, file, indent=4)

    def response_data(self):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={API_KEY}&units=metric"
            response = rq.get(url, timeout=17)
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                self._record_data(temp)
                return int(temp)
            else:
                log.log("warning", f"API вернуло статус {response.status_code}")
                return None
        except Exception as e:
            log.log("error", f"Ошибка при получении данных погоды для города ({self.city}): {e}")
            print("Ошибка при получении данных о погоде", e)
            return None

    def get_weather(self):
        if not self.check_date_request():
            try:
                with open("logic/api/OpenWeatherMap/data_response.json", "r") as file:
                    data = json.load(file)
                    return {
                        "city": self.city,
                        "temp": int(data["temp"])
                    }
            except Exception as e:
                log.log("error", f"Ошибка при чтении json: {e}")
                return {
                    "city": self.city,
                    "temp": None
                }
                
        temp = self.response_data()
        if temp is not None:
            return {
                "city": self.city,
                "temp": temp
            }
        else:
            with open("logic/api/OpenWeatherMap/data_response.json", "r") as file:
                data = json.load(file)
                return {
                    "city": self.city,
                    "temp": int(data["temp"])
                }