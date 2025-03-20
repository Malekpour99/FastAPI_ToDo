from starlette import status
from fastapi import APIRouter

router = APIRouter()

@router.get("/auth/", status_code=status.HTTP_200_OK)
async def get_user():
    return {"user": "authenticated"}

