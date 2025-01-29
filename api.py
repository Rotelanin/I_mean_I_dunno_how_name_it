# :3
import fast_api
from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the API!"}

@app.get("/users/{user_id}", tags=["Users"], summary="Get User Details")
def get_user(user_id: int):
    """Retrieve details of a specific user by their ID."""
    return {"id": user_id, "username": "example_user", "email": "user@example.com"}

@app.post("/users/register", tags=["Users"], summary="Register a New User")
def register_user(username: str, email: str, password: str):
    """Register a new user with a username, email, and password."""
    return {"id": 1, "username": username, "email": email}

@app.delete("/users/{user_id}", tags=["Users"], summary="Delete a User")
def delete_user(user_id: int):
    """Delete a user by their ID."""
    return {"message": "User deleted successfully"}