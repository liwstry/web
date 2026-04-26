# from pydantic import BaseModel, Field, field_validator
# from datetime import date

# class User(BaseModel):
#     id: int
#     name: str
#     birthday_date: date

#     @field_validator('name', mode='before')
#     def validate_name(cls, v):
#         if isinstance(v, int):
#             return str(v)
#         elif isinstance(v, str):
#             return v
#         else:
#             raise ValueError("Имя должно быть строкой или числом")

# import jwt
# from datetime import datetime, timedelta, timezone

# token = jwt.encode({
#             "user_id": 7,
#             "exp": datetime.now(timezone.utc) + timedelta(hours=3)
#         }, "secret_key", algorithm="HS256")
# print(token)

# from dotenv import load_dotenv
# import os

# load_dotenv()
# print(os.getenv("MAIL_PASSWORD"))


# from logic.api.OpenWeatherMap.weather import OpenWeatherAPI
# print(OpenWeatherAPI().get_weather("Москва"))

# from threading import Thread
# from time import sleep

# from logic.api.OpenWeatherMap.weather import OpenWeatherAPI

# inst = OpenWeatherAPI()
# print(inst.get_weather("Москва"))

# import requests as rq
# from config import Config

# API_KEY = Config.API_TOKEN_WEATHER
# city = "London"

# url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
# response = rq.get(url)
# print(response)

# if response.status_code == 200:
#     data = response.json()
#     print(data)
#     temp = data["main"]["temp"]
#     print(temp)



a = "hello"
b = ""
print(True if len(a or b) < 7 else False)




from email_validator import validate_email, EmailNotValidError
from eng_to_ru import Translator

translator = Translator()

email = "abc.@gmail.com"
try:
    validated_email = validate_email(email)
    print("Valid email:", validated_email["email"])
except EmailNotValidError as e:
    print("Invalid email:", translator.run(str(e)))