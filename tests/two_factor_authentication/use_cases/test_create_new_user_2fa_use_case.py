from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.two_factor_authentication.services.users_2fa_service import (
    Users2FAService,
)
from app.two_factor_authentication.use_cases.create_new_user_2fa_use_case import (
    CreateNewUser2FAUseCase,
)
from tests.utils.create_user import create_user
from urllib.parse import quote

settings = get_settings()


class TestCreateNewUser2FAUseCase:
    def test_create_new_user_2fa(self, session: Session) -> None:
        created_user = create_user(session)
        response = CreateNewUser2FAUseCase(session).execute(created_user.email)

        user_2fa = Users2FAService(session).get_by_user_id(created_user.id)

        assert user_2fa

        assert (
            response.provisioning_url
            == f"otpauth://totp/{settings.PROJECT_NAME}:{quote(created_user.email)}?secret={user_2fa.secret_key}&issuer={settings.PROJECT_NAME}"
        )
