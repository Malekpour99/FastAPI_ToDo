from models.users import Users
from dependencies import db_dependency, bcrypt_context

def authenticate_user(*, username: str, password: str, db: db_dependency) -> bool:
    """Authenticate user by the provided credentials"""
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return True

