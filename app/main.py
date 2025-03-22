from fastapi import FastAPI

from routers import auth, todos
from db.database import Base, engine

# Creating database if it doesn't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)

