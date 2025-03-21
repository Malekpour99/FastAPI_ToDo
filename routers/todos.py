from typing import List, Optional

from starlette import status
from pydantic import BaseModel, Field
from fastapi import APIRouter, Path, HTTPException

from models import Todos
from dependencies import db_dependency

class TodoRequest(BaseModel):
    title: str = Field(min_length=2)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: Optional[bool] = False

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_todos(db: db_dependency):
    """Returns all the to-do tasks from the database"""
    return db.query(Todos).all()

@router.get("/todo/{todo_id}/", status_code=status.HTTP_200_OK)
async def get_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    """Returns desired to do task based on its ID"""
    todo_task = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_task:
        return todo_task
    raise HTTPException(status_code=404, detail="Not found")

@router.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest) -> None:
    """Creates a new to-do task"""
    new_todo = Todos(**todo_request.dict())
    db.add(new_todo)
    db.commit()

@router.put("/todo/{todo_id}/", status_code=status.HTTP_204_NO_CONTENT)
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

@router.delete("/todo/{todo_id}/", status_code=status.HTTP_204_NO_CONTENT)
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

