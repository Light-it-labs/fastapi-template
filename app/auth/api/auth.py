from fastapi import APIRouter, HTTPException, status, Response, Request

from app.common.api.dependencies.get_session import SessionDependency
from app.auth.schemas.auth_schema import UserLogin
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

from app.users.repositories.providers_repository import providers_repository
from app.users.repositories.patients_repository import patients_repository


router = APIRouter()
settings = get_settings()

limiter = Limiter(key_func=get_remote_address)


@router.post("/providers/login", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(settings.AUTHENTICATION_API_RATE_LIMIT)
def login_provider_access_token(
    request: Request,
    session: SessionDependency,
    login_data: UserLogin,
    response: Response,
) -> None:
    try:
        AuthUserUseCase(session).execute(
            login_data, response, providers_repository
        )
    except (ModelNotFoundException, InvalidCredentialsException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@router.post("/patients/login", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(settings.AUTHENTICATION_API_RATE_LIMIT)
def login_patient_access_token(
    request: Request,
    session: SessionDependency,
    login_data: UserLogin,
    response: Response,
) -> None:
    try:
        AuthUserUseCase(session).execute(
            login_data, response, patients_repository
        )
    except (ModelNotFoundException, InvalidCredentialsException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@router.post("/logout")
async def logout(response: Response) -> None:
    response.delete_cookie(key="access_token", httponly=True)
