from typing import Annotated, cast
from uuid import UUID

from fastapi import Depends, HTTPException
from starlette import status

from app.auth.enums.claims_enum import ClaimsEnum
from app.auth.schemas.token_schema import TokenPayload
from app.common.api.dependencies.get_session import SessionDependency
from app.auth.api.dependencies.get_token import TokenDep

from app.auth.utils.security import validate_token
from app.auth.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.users.schemas.user_schema import UserInDB
from app.users.services.users_service import UsersService


def get_current_user(session: SessionDependency, token: TokenDep) -> UserInDB:
    try:
        token_data = cast(
            TokenPayload, validate_token(token, ClaimsEnum.USER_ID)
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message
        )
    provider = UsersService(session).get_by_id(UUID(token_data.user_id))
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


CurrentUser = Annotated[UserInDB, Depends(get_current_user)]
