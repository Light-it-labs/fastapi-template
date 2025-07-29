from typing import cast
from sqlalchemy.orm import Session

from app.auth.enums.claims_enum import ClaimsEnum
from app.auth.schemas.token_schema import EmailTokenPayload
from app.auth.services.auth_service import AuthService
from app.auth.utils.security import get_password_hash, validate_token


class ResetPasswordUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(self, token: str, password: str) -> None:
        token_data = cast(
            EmailTokenPayload, validate_token(token, ClaimsEnum.USER_EMAIL)
        )
        hashed_password = get_password_hash(password)
        AuthService(self.session).reset_password(
            token_data.user_email, hashed_password
        )
