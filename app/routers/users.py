from typing import Annotated

from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.models.users import Users
from app.dependencies import db_dependency
from app.common.exceptions import CREDENTIALS_EXCEPTION
from app.services.auth import authenticate_user, user_dependency
from app.core.security import (
    hash_password,
    match_passwords,
    create_access_token,
)
from app.schemas.users import (
    Token,
    UserInfo,
    CreateUserRequest,
    ChangePasswordRequest,
)

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
    user = authenticate_user(
        username=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect Username or Password",
        )
    access_token = create_access_token(user=user, expires_delta=20)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/info/", response_model=UserInfo, status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency, db: db_dependency):
    """Returns authenticated user's information"""
    if not user:
        raise CREDENTIALS_EXCEPTION

    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.post("/change-password/", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_password(
    user: user_dependency,
    db: db_dependency,
    change_password_request: ChangePasswordRequest,
) -> None:
    """Change authenticated user's password"""
    if not user:
        raise CREDENTIALS_EXCEPTION

    user_data = db.query(Users).filter(Users.id == user.get("id")).first()
    # Wrong password
    if not match_passwords(
        main_password=user_data.password,
        entered_password=change_password_request.old_password,
    ):
        raise HTTPException(status_code=400, detail="Wrong password")
    # Identical new passwrod and old password
    if match_passwords(
        main_password=user_data.password,
        entered_password=change_password_request.new_password,
    ):
        raise HTTPException(
            status_code=400,
            detail="New password can not be the same as your old password",
        )
    # Unmatched new passwords
    if (
        not change_password_request.new_password
        == change_password_request.new_password_confirm
    ):
        raise HTTPException(
            status_code=400,
            detail="New passwords & its confirmation didn't match",
        )

    user_data.password = hash_password(
        password=change_password_request.new_password,
    )

    db.add(user_data)
    db.commit()
