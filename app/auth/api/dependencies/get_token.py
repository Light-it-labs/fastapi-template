from typing import Annotated

from fastapi import Depends


from app.auth.api.dependencies.oauth2_password_bearer_with_cookie import (
    OAuth2PasswordBearerWithCookie,
)
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl=f"{settings.API_V1_STR}/login"
)

TokenDep = Annotated[str, Depends(oauth2_scheme)]
