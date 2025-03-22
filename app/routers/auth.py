from typing import Annotated

from starlette import status
from passlib.context import CryptContext
from fastapi import APIRouter, Path, Depends, HTTPException

from models.users import Users
from dependencies import db_dependency
from schemas.users import CreateUserRequest

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post("/user/", status_code=status.HTTP_201_CREATED)
async def create_user(
        db: db_dependency,
        create_user_request: CreateUserRequest,
        ) -> None:
    """Create new users"""
    user = Users(**create_user_request.model_dump())
    # hashing user password
    user.password = bcrypt_context.hash(create_user_request.password)
    db.add(user)
    db.commit()

