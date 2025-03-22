from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import SessionLocal
from passlib.context import CryptContext

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

# for Hashing passwords
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

