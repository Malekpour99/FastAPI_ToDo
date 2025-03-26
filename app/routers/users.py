from typing import Annotated

from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Path, Depends, HTTPException

from app.models.users import Users
from app.dependencies import db_dependency
from app.services.auth import authenticate_user
from app.schemas.users import CreateUserRequest, Token
from app.core.security import hash_password, create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
        db: db_dependency,
        create_user_request: CreateUserRequest,
        ) -> None:
    """Create new users"""
    user = Users(**create_user_request.model_dump())
    # hashing user password
    user.password = hash_password(password=create_user_request.password)
    db.add(user)
    db.commit()

@router.post("/token/", response_model=Token, status_code=status.HTTP_200_OK)
async def get_tokens(
        db: db_dependency,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        ):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect Username or Password")
    access_token = create_access_token(user=user, expires_delta=20)
    return {"access_token": access_token, "token_type": "bearer"}

