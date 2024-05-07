from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from app.api.dependencies.get_db import SessionDependency
from app.api.dependencies.get_token import TokenDep
from app.core.security import validate_token
from app.exceptions.invalid_credentials_exception import InvalidCredentialsException
from app.repositories.users_repository import users_repository
from app.schemas.user_schema import UserInDBBase
from app.services.users_service import UsersService


def get_current_user(session: SessionDependency, token: TokenDep) -> UserInDBBase:
    try:
        token_data = validate_token(token)
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    provider = UsersService(session, users_repository).get_by_id(token_data.user_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


CurrentUser = Annotated[UserInDBBase, Depends(get_current_user)]
