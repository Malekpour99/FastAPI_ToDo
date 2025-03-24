from typing import Union
from datetime import datetime, timedelta

from jose import jwt

from models.users import Users
from dependencies import db_dependency
from core.security import match_passwords
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def authenticate_user(*, username: str, password: str, db: db_dependency) -> Union[Users, bool]:
    """Authenticate user by the provided credentials"""
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not match_passwords(main_password=user.password, entered_password=password):
        return False
    return user

def create_access_token(*, user: Users, expires_delta: int = None) -> str:
    """Creates JWT access token"""

    to_encode = {
            "sub": user.username,
            "id": user.id,
            "exp": datetime.utcnow() + timedelta(
                minutes=expires_delta if expires_delta else ACCESS_TOKEN_EXPIRE_MINUTES
                ),
            }

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

