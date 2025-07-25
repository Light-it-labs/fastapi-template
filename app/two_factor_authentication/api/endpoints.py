from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from slowapi import Limiter

from app.common.api.dependencies.get_session import SessionDependency
from app.common.exceptions.model_not_created_exception import (
    ModelNotCreatedException,
)
from app.core.config import get_settings

from slowapi.util import get_remote_address

from app.two_factor_authentication.schemas.user_2fa_schema import (
    User2FAResponse,
)
from app.two_factor_authentication.use_cases.create_new_user_2fa_use_case import (
    CreateNewUser2FAUseCase,
)


router = APIRouter()
settings = get_settings()

limiter = Limiter(key_func=get_remote_address)


@router.post("/totp", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(settings.AUTHENTICATION_API_RATE_LIMIT)
def create_new_user_2fa(
    session: SessionDependency, user_id: UUID
) -> User2FAResponse:
    try:
        return CreateNewUser2FAUseCase(session).execute(user_id)
    except ModelNotCreatedException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )
