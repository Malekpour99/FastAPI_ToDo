from typing import Union, Annotated
from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, Depends, HTTPException

from app.models.users import Users
from app.dependencies import db_dependency
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# for Hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# for decoding JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(*, password: str) -> str:
    """Create a hash from the given password"""
    return pwd_context.hash(password)

def match_passwords(*, main_password: str, entered_password: str) -> bool:
    """Verifies password hashes are matched"""
    return pwd_context.verify(entered_password, main_password)

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

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Gets current user based on the decoded token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM)
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise credentials_exception
        return {"username": username, "user_id": user_id}

    except JWTError:
        raise credentials_exception

