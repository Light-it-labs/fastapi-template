from fastapi import APIRouter, HTTPException, status, Response, Request

from app.api.dependencies.get_db import SessionDependency
from app.core.config import get_settings
from app.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.exceptions.model_not_found_exception import ModelNotFoundException
from app.schemas.auth_schema import UserLogin
from app.use_cases.auth_user_use_case import AuthUserUseCase
from slowapi import Limiter
from slowapi.util import get_remote_address


router = APIRouter()
settings = get_settings()

limiter = Limiter(key_func=get_remote_address)


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(settings.AUTHENTICATION_API_RATE_LIMIT)
def login_access_token(
    request: Request,
    session: SessionDependency,
    login_data: UserLogin,
    response: Response,
) -> None:
    try:
        AuthUserUseCase(session).execute(login_data, response)
    except (ModelNotFoundException, InvalidCredentialsException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@router.post("/logout")
async def logout(response: Response) -> None:
    response.delete_cookie(key="access_token", httponly=True)
