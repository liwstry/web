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

user_count = 7
admin_count = 2
users = ["user1", "user2", "user3", "user4", "user5", "user6", "user7"]
a = {"user_count": user_count,
            "admin_count": admin_count,
            "users": users}
print(a)