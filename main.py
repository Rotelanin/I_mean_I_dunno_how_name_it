from fastapi import FastAPI, HTTPException
from models import User, Team, Match, Result

app = FastAPI()

@app.post("/register", summary="Реєстрація користувача")
def reg_user():
    pass

@app.post("/team", summary="Команда")
def reg_team():
    pass

@app.get("/match", summary="Турнір")
def add_match():
    pass

@app.get("/users", summary="Список користувачів")
def get_users():
    pass

@app.get("/teams", summary="Список команд")
def get_teams():
    pass
