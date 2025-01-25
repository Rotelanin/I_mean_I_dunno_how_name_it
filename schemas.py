# зробіть тут валідацію. та решта що в завданні пише <3

from pydantic import BaseModel, EmailStr
from typing import List, Optional

class User(BaseModel):
    name: str = Query(description="User name", max_length=24, min_length=2)
    password: str
    email: EmailStr
    @field_validator("password")
    @classmethod
    def password_validator(cls, value):
        if len(value) < 8:
            raise ValueError("Пароль занадто короткий!")
        if not any(char in "!@#$%^&*_" for char in value):
            raise ValueError("В паролі має бути спеціальний символ")
        if not any(char.isupper() for char in value):
            raise ValueError("В паролі має бути хочаб одна велика буква.")

class Team(BaseModel):
    team_name: str = Query(description="User name", max_length=24, min_length=2)
    members: List[User]
    TeamLead: User

class Tournament(BaseModel):
    teams: List[Team] 
    name: str = Query(description="Tournament name", max_length=24, min_length=2)
    winner: Team
    losers: List[Team]

    @model_validator(mode="before")
    @classmethod
    def check_all(cls, values):
        teams = values.get("teams")
        losers: List = values.get("losers")

        if len(losers) >= len(teams):
            raise ValueError("Неправильна кількість юзерів")