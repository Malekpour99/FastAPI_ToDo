from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from app.models.users import Users
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# for Hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# for decoding JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

def hash_password(*, password: str) -> str:
    """Create a hash from the given password"""
    return pwd_context.hash(password)

def match_passwords(*, main_password: str, entered_password: str) -> bool:
    """Verifies password hashes are matched"""
    return pwd_context.verify(entered_password, main_password)

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

