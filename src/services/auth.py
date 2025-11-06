import jwt
import hashlib
import secrets

from datetime import datetime, timedelta
from passlib.context import CryptContext

from src import config, logger


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    salt, hashed = hashed_password.split(":")

    return hashed == hashlib.sha256((plain_password + salt).encode()).hexdigest()

def get_password_hash(password: str) -> str:
    """Хеширование пароля"""
    salt = secrets.token_hex(16)
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

    return f'{salt}:{hashed_password}'


def create_access_token(data: dict) -> str:
    """Создание JWT токена"""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    to_encode['sub'] = str(to_encode['sub'])

    encoded_jwt = jwt.encode(
        to_encode,
        config.SECRET_KEY,
        algorithm=config.ALGORITHM
    )

    logger.info(f"Токен доступа создан для: {data.get('sub')}")

    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Декодирование JWT токена"""
    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.ALGORITHM]
        )
        return payload
    except Exception as e:
        logger.error(f"Ошибка чтения JWT токена: {e}")
        raise


__all__ = [
    'verify_password',
    'get_password_hash',
    'create_access_token',
    'decode_access_token',
]
