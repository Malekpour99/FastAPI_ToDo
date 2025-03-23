from passlib.context import CryptContext

# for Hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(*, password: str) -> str:
    """Create a hash from the given password"""
    return pwd_context.hash(password)

def match_passwords(*, main_password: str, entered_password: str) -> bool:
    """Verifies password hashes are matched"""
    return pwd_context.verify(entered_password, main_password)

