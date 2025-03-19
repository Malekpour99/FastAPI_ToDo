from typing import List, Annotated, Optional

from starlette import status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi import FastAPI, Path, Depends, HTTPException

from models import Base, Todos
from database import engine, SessionLocal

app = FastAPI()

# Creating database if it doesn't exist
Base.metadata.create_all(bind=engine)


def get_db():
    """
    Connects to the database 
    then closes its connection after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=2)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: Optional[bool] = False


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all_todos(db: db_dependency):
    """Returns all the to-do tasks from the database"""
    return db.query(Todos).all()

@app.get("/todo/{todo_id}/", status_code=status.HTTP_200_OK)
async def get_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    """Returns desired to do task based on its ID"""
    todo_task = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_task:
        return todo_task
    raise HTTPException(status_code=404, detail="Not found")

@app.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest) -> None:
    new_todo = Todos(**todo_request.dict())
    db.add(new_todo)
    db.commit()

@app.put("/todo/{todo_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
        db: db_dependency,
        todo_request: TodoRequest,
        todo_id: int = Path(gt=0),
        ) -> None:
    todo_task = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_task:
        raise HTTPException(status_code=404, detail="Not found")

    todo_task.title = todo_request.title
    todo_task.description = todo_request.description
    todo_task.priority = todo_request.priority
    todo_task.complete = todo_request.complete

    db.add(todo_task)
    db.commit()

@app.delete("/todo/{todo_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        db: db_dependency,
        todo_id: int = Path(gt=0),
        ) -> None:
    todo_task = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_task:
        raise HTTPException(status_code=404, detail="Not found")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

