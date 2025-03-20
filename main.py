from fastapi import FastAPI

from models import Base
from database import engine
from routers import auth, todos

# Creating database if it doesn't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)

