from starlette import status
from fastapi import APIRouter, Path, Depends, HTTPException

from app.models.todos import Todos
from app.dependencies import db_dependency
from app.services.auth import user_dependency
from app.common.exceptions import CREDENTIALS_EXCEPTION

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/todo/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    """Returns every available to do task for admin user"""
    if not user:
        raise CREDENTIALS_EXCEPTION
    if not user.get("role") == "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Permission Denied")

    return db.query(Todos).all()

@router.delete("/todo/{todo_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        user: user_dependency,
        db: db_dependency,
        todo_id: int = Path(gt=0)
        ) -> None:
    """Deletes desired to do task"""
    if not user:
        raise CREDENTIALS_EXCEPTION
    if not user.get("role") == "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Permission Denied")

    todo_task = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_task:
        raise HTTPException(status_code=404, detail="Not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

