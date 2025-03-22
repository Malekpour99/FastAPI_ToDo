from typing import Optional

from starlette import status
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from fastapi import APIRouter, Path, HTTPException

from models import Users
from dependencies import db_dependency

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUserRequest(BaseModel):
    email: str = Field(min_length=6)
    username: str = Field(min_length=1, max_length=20)
    first_name: str = Field(min_length=1, max_length=30)
    last_name: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=8, max_length=100)
    role: str = Field(min_length=1, max_length=30)
    is_active: Optional[bool] = True


router = APIRouter()

@router.post("/user/", status_code=status.HTTP_201_CREATED)
async def create_user(
        db: db_dependency,
        create_user_request: CreateUserRequest,
        ) -> None:
    """Creating new users with hashed passwords"""
    user = Users(**create_user_request.model_dump())
    user.password = bcrypt_context.hash(create_user_request.password)
    db.add(user)
    db.commit()

