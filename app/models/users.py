from sqlalchemy import Column, Integer, String, Boolean

from app.db.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    phone_number = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
