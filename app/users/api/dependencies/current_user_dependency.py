__all__ = (
    "get_current_user",
    "CurrentUserDependency",
)

import typing as t

import fastapi

from app.auth.api.dependencies.get_token import TokenDep
from app.auth.enums.claims_enum import ClaimsEnum
from app.auth.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.auth.schemas.token_schema import TokenPayload
from app.auth.utils.security import validate_token
from app.common.exceptions import ModelNotFoundException
from app.users.domain import User
from app.users.domain import UserId

from .user_repository_dependency import UserRepositoryDependency


def get_current_user(
    user_repository: UserRepositoryDependency,
    token: TokenDep,
) -> User:
    try:
        token_data = t.cast(
            TokenPayload, validate_token(token, ClaimsEnum.USER_ID)
        )
    except InvalidCredentialsException as e:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail=e.message
        )

    try:
        user = user_repository.find_or_fail(UserId(token_data.user_id))
    except ModelNotFoundException as e:
        raise fastapi.HTTPException(
            status_code=404,
            detail=e.message,
        )

    return user


CurrentUserDependency = t.Annotated[
    User,
    fastapi.Depends(get_current_user),
]
