import unittest
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
from jose import jwt, JWTError
from datetime import datetime, timedelta
from I_mean_I_dunno_how_name_it.database import get_db, create_user, get_user_by_id
from I_mean_I_dunno_how_name_it.models import User
from I_mean_I_dunno_how_name_it.schemas import UserSchema

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class TestDatabase(unittest.TestCase):
    def test_database_connection(self):
        try:
            db = next(get_db())
            self.assertIsNotNone(db)
        except SQLAlchemyError:
            self.fail("Database connection failed")

class TestUserModel(unittest.TestCase):
    def test_user_model(self):
        user = User(id=1, username="test_user", email="test@example.com", password="hashedpassword")
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test@example.com")

class TestUserSchema(unittest.TestCase):
    def test_user_schema_valid(self):
        user_data = {"username": "valid_user", "email": "valid@example.com", "password": "securepassword"}
        user = UserSchema(**user_data)
        self.assertEqual(user.username, "valid_user")
        self.assertEqual(user.email, "valid@example.com")

    def test_user_schema_invalid(self):
        with self.assertRaises(ValidationError):
            UserSchema(username="", email="invalid", password="123")

class TestUserFunctions(unittest.TestCase):
    def test_create_user(self):
        db = next(get_db())
        user = create_user(db, username="new_user", email="new@example.com", password="securepassword")
        self.assertEqual(user.username, "new_user")
        self.assertEqual(user.email, "new@example.com")

    def test_get_user_by_id(self):
        db = next(get_db())
        user = create_user(db, username="lookup_user", email="lookup@example.com", password="securepassword")
        fetched_user = get_user_by_id(db, user.id)
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.username, "lookup_user")

class TestJWTAuthentication(unittest.TestCase):
    def test_create_access_token(self):
        token = create_access_token({"sub": "test_user"})
        self.assertIsInstance(token, str)

    def test_decode_access_token(self):
        token = create_access_token({"sub": "test_user"})
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            self.assertEqual(decoded["sub"], "test_user")
        except JWTError:
            self.fail("Token decoding failed")

if __name__ == "__main__":
    unittest.main()