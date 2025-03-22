from typing import Optional

from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    email: str = Field(min_length=6)
    username: str = Field(min_length=1, max_length=20)
    first_name: str = Field(min_length=1, max_length=30)
    last_name: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=8, max_length=100)
    role: str = Field(min_length=1, max_length=30)
    is_active: Optional[bool] = True

