from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from starlette import status

from app.common.api.dependencies.get_session import SessionDependency
from app.auth.api.dependencies.get_token import TokenDep

from app.auth.utils.security import validate_token
from app.auth.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.users.schemas.user_schema import UserInDB
from app.users.services.providers_service import ProvidersService
from app.users.repositories.providers_repository import providers_repository


def get_current_provider(
    session: SessionDependency, token: TokenDep
) -> UserInDB:
    try:
        token_data = validate_token(token)
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=e.message
        )
    provider = ProvidersService(session, providers_repository).get_by_id(
        UUID(token_data.user_id)
    )
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


CurrentProvider = Annotated[UserInDB, Depends(get_current_provider)]
