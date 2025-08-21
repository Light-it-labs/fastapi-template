from sqlalchemy.orm import Session
import pyotp
from app.common.exceptions.model_not_found_exception import (
    ModelNotFoundException,
)
from app.core.config import get_settings
from app.two_factor_authentication.schemas.user_2fa_schema import (
    VerifyUser2FAData,
)
from app.two_factor_authentication.services.users_2fa_service import (
    Users2FAService,
)
from app.users.services.users_service import UsersService

settings = get_settings()


class VerifyUser2FAUseCase:
    def __init__(self, session: Session):
        self.session = session
        self.users_service = UsersService(self.session)
        self.users_2fa_service = Users2FAService(self.session)

    def execute(self, data: VerifyUser2FAData) -> bool:
        user = self.users_service.get_by_id(data.user_id)
        if not user:
            raise ModelNotFoundException("User not found")

        user_2fa = self.users_2fa_service.get_by_user_id(user.id)

        if not user_2fa:
            raise ModelNotFoundException("User 2FA not found")

        if data.mark_active:
            self.users_2fa_service.toggle_active(user_2fa.id, True)

        totp = pyotp.TOTP(user_2fa.secret_key)

        return totp.verify(data.user_code)
