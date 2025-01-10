# зробіть тут валідацію. та решта що в завданні пише <3

from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    password: str
    email: str

class Team(BaseModel):
    id: int
    team_name: str
    members: str

class Match(BaseModel):
    id: int
    name: str
    start_date: str
    end_date: str
    teams: str
    status: bool

class Result(BaseModel):
    win: str
    date: int
