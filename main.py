from typing import List, Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

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

@app.get("/")
async def read_all_todos(db: db_dependency):
    """Returns all the to-do tasks from the database"""
    return db.query(Todos).all()

