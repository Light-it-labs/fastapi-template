from fastapi import APIRouter, HTTPException, status

from app.api.dependencies.get_db import SessionDependency
from app.core.config import get_settings
from app.core.security import create_access_token
from app.exceptions.invalid_credentials_exception import InvalidCredentialsException
from app.exceptions.model_not_found_exception import ModelNotFoundException
from app.repositories.users_repository import users_repository
from app.schemas.auth_schema import UserLogin
from app.schemas.token_schema import Token, TokenPayload
from app.services.auth_service import AuthService
from app.use_cases.auth_user_use_case import AuthUserUseCase

router = APIRouter()
settings = get_settings()


@router.post("/login")
def login_access_token(session: SessionDependency, login_data: UserLogin) -> Token:
    try:
        return AuthUserUseCase(session).execute(login_data)
    except (ModelNotFoundException, InvalidCredentialsException):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
