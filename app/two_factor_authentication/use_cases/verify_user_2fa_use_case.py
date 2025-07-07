from sqlalchemy.orm import Session
import pyotp
from app.common.exceptions.model_not_found_exception import (
    ModelNotFoundException,
)
from app.core.config import get_settings
from app.two_factor_authentication.repositories.user_2fa_repository import (
    users_2fa_repository,
)
from app.two_factor_authentication.schemas.user_2fa_schema import (
    VerifyUser2FARequest,
)
from app.two_factor_authentication.services.user_2fa_service import (
    Users2FAService,
)
from app.users.repositories.users_repository import users_repository
from app.users.services.users_service import UsersService

settings = get_settings()


class VerifyUser2FAUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(self, data: VerifyUser2FARequest) -> bool:
        user = UsersService(self.session, users_repository).get_by_id(
            data.user_id
        )
        if not user:
            raise ModelNotFoundException("User not found")

        user_2fa = Users2FAService(
            self.session, users_2fa_repository
        ).get_by_user_id(user.id)

        if not user_2fa:
            raise ModelNotFoundException("User 2FA not found")

        totp = pyotp.TOTP(user_2fa.secret_key)

        return totp.verify(data.user_code)
