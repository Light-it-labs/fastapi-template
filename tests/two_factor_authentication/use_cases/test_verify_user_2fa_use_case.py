import pyotp
from sqlalchemy.orm import Session

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
from app.two_factor_authentication.use_cases.create_new_user_2fa_use_case import (
    CreateNewUser2FAUseCase,
)
from app.two_factor_authentication.use_cases.verify_user_2fa_use_case import (
    VerifyUser2FAUseCase,
)
from tests.utils.create_user import create_user

settings = get_settings()


class TestVerifyUser2FAUseCase:
    def test_verify_correct_user_2fa(self, session: Session) -> None:
        created_user = create_user(session)
        CreateNewUser2FAUseCase(session).execute(created_user.email)

        user_2fa = Users2FAService(
            session, users_2fa_repository
        ).get_by_user_id(created_user.id)

        assert user_2fa

        totp = pyotp.TOTP(user_2fa.secret_key)
        valid_code = totp.now()

        data = VerifyUser2FARequest(
            user_id=created_user.id, user_code=valid_code
        )
        is_valid = VerifyUser2FAUseCase(session).execute(data)

        assert is_valid

    def test_verify_incorrect_user_2fa(self, session: Session) -> None:
        created_user = create_user(session)
        CreateNewUser2FAUseCase(session).execute(created_user.email)

        invalid_code = "000000"
        data = VerifyUser2FARequest(
            user_id=created_user.id, user_code=invalid_code
        )
        is_valid = VerifyUser2FAUseCase(session).execute(data)

        assert not is_valid
