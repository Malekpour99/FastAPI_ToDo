from models.users import Users
from dependencies import db_dependency
from core.security import match_passwords

def authenticate_user(*, username: str, password: str, db: db_dependency) -> bool:
    """Authenticate user by the provided credentials"""
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not match_passwords(main_password=user.password, entered_password=password):
        return False
    return True

