from typing import Annotated
from fastapi import APIRouter, HTTPException, Header, status, Response, Request

from app.auth.use_cases.reset_password_use_case import ResetPasswordUseCase
from app.common.api.dependencies.get_session import SessionDependency
from app.auth.schemas.auth_schema import PasswordResetRequest, UserLogin
from app.auth.use_cases.auth_user_use_case import AuthUserUseCase
from app.common.exceptions.model_not_found_exception import (
    ModelNotFoundException,
)
from app.core.config import get_settings
from app.auth.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
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


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(settings.AUTHENTICATION_API_RATE_LIMIT)
def reset_password(
    request: Request,
    session: SessionDependency,
    token: Annotated[str, Header()],
    body: PasswordResetRequest,
) -> None:
    try:
        ResetPasswordUseCase(session).execute(token, body.password)
    except (InvalidCredentialsException, ModelNotFoundException) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=e.message
        )
