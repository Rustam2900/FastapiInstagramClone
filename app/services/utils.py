from passlib.context import CryptContext

from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(password, hash_password):
    return pwd_context.verify(password, hash_password)
