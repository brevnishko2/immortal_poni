from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TODO: Подключить Redis для хранения blacklist
token_blacklist = set()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )
    return encoded_jwt


def blacklist_token(token: str, expires: int):
    """Добавляем токен в черный список"""
    token_blacklist.add(token)


def is_token_blacklisted(token: str) -> bool:
    """Проверяем, находится ли токен в черном списке"""
    return token in token_blacklist
