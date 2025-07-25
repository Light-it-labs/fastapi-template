from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from slowapi import Limiter

from app.common.api.dependencies.get_session import SessionDependency
from app.common.exceptions.model_not_created_exception import (
    ModelNotCreatedException,
)
from app.common.exceptions.model_not_found_exception import (
    ModelNotFoundException,
)
from app.core.config import get_settings

from slowapi.util import get_remote_address

from app.two_factor_authentication.schemas.user_2fa_schema import (
    User2FAResponse,
    VerifyUser2FAData,
    VerifyUser2FARequest,
)
from app.two_factor_authentication.use_cases.create_new_user_2fa_use_case import (
    CreateNewUser2FAUseCase,
)
from app.two_factor_authentication.use_cases.verify_user_2fa_use_case import (
    VerifyUser2FAUseCase,
)


router = APIRouter()
settings = get_settings()

limiter = Limiter(key_func=get_remote_address)


@router.post("", status_code=status.HTTP_200_OK)
def create_new_user_2fa(
    session: SessionDependency, user_id: UUID
) -> User2FAResponse:
    try:
        return CreateNewUser2FAUseCase(session).execute(user_id)
    except ModelNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except ModelNotCreatedException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )


@router.post("/verify", status_code=status.HTTP_200_OK)
def verify_user_2fa(
    session: SessionDependency, user_id: UUID, request: VerifyUser2FARequest
) -> None:
    try:
        valid_2fa = VerifyUser2FAUseCase(session).execute(
            VerifyUser2FAData(user_id=user_id, **request.model_dump())
        )
        if not valid_2fa:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid 2FA code provided.",
            )
    except ModelNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
