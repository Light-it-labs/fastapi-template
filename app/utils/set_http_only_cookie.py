from uuid import UUID

from fastapi import Response

from app.core import security
from app.core.config import get_settings
from app.schemas.token_schema import TokenPayload

settings = get_settings()


def set_http_only_cookie(user_id: UUID, key: str, response: Response) -> None:
    access_token = security.create_access_token(
        TokenPayload(user_id=str(user_id))
    )
    response.set_cookie(
        key=key,
        value=access_token,
        httponly=True,
        secure=settings.SECURE_COOKIE,
        samesite="lax",
    )
