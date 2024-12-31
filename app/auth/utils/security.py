from datetime import datetime, timedelta
from typing import Any

import bcrypt
import pytz
from jwt import encode, decode
from jwt.exceptions import PyJWTError
from pydantic import ValidationError
from app.auth.api.dependencies.get_token import TokenDep
from app.auth.schemas.token_schema import TokenPayload
from app.core.config import settings
from app.auth.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)


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
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def validate_token(token: TokenDep) -> TokenPayload:
    if not token:
        raise InvalidCredentialsException()
    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
        token_data = TokenPayload(**payload)
    except (PyJWTError, ValidationError):
        raise InvalidCredentialsException()
    return token_data
