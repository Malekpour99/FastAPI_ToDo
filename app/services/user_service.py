from typing import Annotated

from jose import jwt, JWTError
from fastapi import status, Depends, HTTPException

from app.core.security import oauth2_scheme 
from app.core.config import SECRET_KEY, ALGORITHM

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

