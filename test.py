from pydantic import BaseModel, Field, field_validator
from datetime import date

class User(BaseModel):
    id: int
    name: str
    birthday_date: date

    @field_validator('name', mode='before')
    def validate_name(cls, v):
        if isinstance(v, int):
            return str(v)
        elif isinstance(v, str):
            return v
        else:
            raise ValueError("Имя должно быть строкой или числом")
