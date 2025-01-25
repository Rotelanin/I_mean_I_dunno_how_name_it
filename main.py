from fastapi import FastAPI, HTTPException
from schemas import User, Team, Tournament
from routers import users

app = FastAPI()
app.include_router(users.router)