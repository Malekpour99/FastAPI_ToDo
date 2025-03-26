from typing import Union, Annotated

from jose import jwt, JWTError
from fastapi import status, Depends, HTTPException

from app.models.users import Users
from app.dependencies import db_dependency
from app.core.config import SECRET_KEY, ALGORITHM
from app.common.exceptions import CREDENTIALS_EXCEPTION
from app.core.security import match_passwords, oauth2_scheme

def authenticate_user(*, username: str, password: str, db: db_dependency) -> Union[Users, bool]:
    """Authenticate user by the provided credentials"""
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not match_passwords(main_password=user.password, entered_password=password):
        return False
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Gets current user based on the decoded token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise CREDENTIALS_EXCEPTION
        return {"username": username, "id": user_id, "role": user_role}

    except JWTError:
        raise CREDENTIALS_EXCEPTION

# for User dependency injection
user_dependency = Annotated[dict, Depends(get_current_user)]

