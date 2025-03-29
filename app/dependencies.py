from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal


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


# for Dependency injection
db_dependency = Annotated[Session, Depends(get_db)]
