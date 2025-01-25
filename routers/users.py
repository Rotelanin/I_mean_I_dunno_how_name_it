from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserPydantic
from jose import jwt, JWTError


SECRET_KEY = "IHGDJFoi8S&DtfsDGBGKLFksDGfj"
ALGORITHM = "HS256"

router = APIRouter()

user_encoded_data = jwt.encode({"username": "Denis"}, SECRET_KEY, ALGORITHM)
print(user_encoded_data)

user_decoded_data = jwt.decode(user_encoded_data, SECRET_KEY, ALGORITHM)
print(user_decoded_data)


@router.get("/users", summary="Отримати всіх юзерів з бд")
async def users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/user/{id_user}", summary="Отримати інформацію про юзера по id")
async def user(id_user: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/user", summary="Тут потім напишу")
async def new_user(user: UserPydantic, db: Session = Depends(get_db)):
    check_user = db.query(User).filter(User.email == user.email).first()
    if check_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    return new_user

@router.delete("/user/{id_user}", summary="Видалити юзера по айді")
async def delete_user(id_user: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}
