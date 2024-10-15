from datetime import datetime, timedelta
from typing import Any

import bcrypt
import pytz
from jose import jwt
from pydantic import ValidationError

from app.api.dependencies.get_token import TokenDep
from app.core.config import settings
from app.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.schemas.token_schema import TokenPayload


def create_access_token(
    token_data: TokenPayload | Any, expires_delta: timedelta | None = None
) -> str:
    if expires_delta:
        expire = datetime.now(pytz.utc) + expires_delta
    else:
        expire = datetime.now(pytz.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire}
    to_encode.update(token_data.model_dump())
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    print(plain_password.encode())
    print(hashed_password.encode())
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    print("HASH")
    print(bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode())
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def validate_token(token: TokenDep):
    if not token:
        raise InvalidCredentialsException()
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise InvalidCredentialsException()
    return token_data
