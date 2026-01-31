from typing import Annotated, cast

from fastapi import Depends
from fastapi import HTTPException
from starlette import status

from app.auth.api.dependencies.get_token import TokenDep
from app.auth.enums.claims_enum import ClaimsEnum
from app.auth.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.auth.schemas.token_schema import TokenPayload
from app.auth.utils.security import validate_token
from app.common.api.dependencies.get_session import SessionDependency
from app.users.domain import User
from app.users.domain.user_types import UserId
from app.users.infrastructure import SQLAlchemyUserRepository


def get_current_user(session: SessionDependency, token: TokenDep) -> User:
    try:
        token_data = cast(
            TokenPayload, validate_token(token, ClaimsEnum.USER_ID)
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message
        )
    user = SQLAlchemyUserRepository(session).find(UserId(token_data.user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Provider not found")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
