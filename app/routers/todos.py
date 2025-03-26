from typing import Annotated

from starlette import status
from fastapi import APIRouter, Path, Depends, HTTPException

from app.models.todos import Todos
from app.schemas.todos import TodoRequest
from app.dependencies import db_dependency
from app.services.auth import user_dependency
from app.common.exceptions import CREDENTIALS_EXCEPTION

router = APIRouter(prefix="/todos", tags=["To-dos"])

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    """Returns all the to-do tasks from the database"""
    if not user:
        raise CREDENTIALS_EXCEPTION
    return db.query(Todos).filter(Todos.owner == user.get("id")).all()

@router.get("/{todo_id}/", status_code=status.HTTP_200_OK)
async def get_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    """Returns desired to do task based on its ID"""
    todo_task = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_task:
        return todo_task
    raise HTTPException(status_code=404, detail="Not found")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(
        db: db_dependency,
        user: user_dependency,
        todo_request: TodoRequest
        ) -> None:
    """Creates a new to-do task"""
    if not user:
        raise CREDENTIALS_EXCEPTION

    new_todo = Todos(**todo_request.dict(), owner=user.get("id"))
    db.add(new_todo)
    db.commit()

@router.put("/{todo_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
        db: db_dependency,
        todo_request: TodoRequest,
        todo_id: int = Path(gt=0),
        ) -> None:
    """Updates desired to-do task based on its ID and provided data"""
    todo_task = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_task:
        raise HTTPException(status_code=404, detail="Not found")

    todo_task.title = todo_request.title
    todo_task.description = todo_request.description
    todo_task.priority = todo_request.priority
    todo_task.complete = todo_request.complete

    db.add(todo_task)
    db.commit()

@router.delete("/{todo_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        db: db_dependency,
        todo_id: int = Path(gt=0),
        ) -> None:
    """Deletes desired to-do task based on its ID"""
    todo_task = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_task:
        raise HTTPException(status_code=404, detail="Not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

