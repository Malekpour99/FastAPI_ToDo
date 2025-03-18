from typing import List, Annotated

from starlette import status
from sqlalchemy.orm import Session
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

