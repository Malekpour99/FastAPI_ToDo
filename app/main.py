from fastapi import FastAPI

from app.internal import admin
from app.routers import users, todos
from app.db.database import Base, engine

# Creating database if it doesn't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(todos.router)
app.include_router(admin.router)

