from fastapi.testclient import TestClient
import pyotp
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.two_factor_authentication.services.users_2fa_service import (
    Users2FAService,
)
from app.two_factor_authentication.use_cases.create_new_user_2fa_use_case import (
    CreateNewUser2FAUseCase,
)
from tests.utils.create_user import create_user

settings = get_settings()


class TestVerifyUser2FAEndpoint:
    def test_verify_correct_user_2fa(
        self, client: TestClient, session: Session
    ) -> None:
        created_user = create_user(session)
        CreateNewUser2FAUseCase(session).execute(created_user.id)

        user_2fa = Users2FAService(session).get_by_user_id(created_user.id)

        assert user_2fa

        totp = pyotp.TOTP(user_2fa.secret_key)
        valid_code = totp.now()

        response = client.post(
            f"api/v1/users/{created_user.id}/totp/verify",
            json={"user_code": valid_code},
        )

        assert response.status_code == 200

    def test_verify_correct_user_2fa_and_mark_active(
        self, client: TestClient, session: Session
    ) -> None:
        created_user = create_user(session)
        CreateNewUser2FAUseCase(session).execute(created_user.id)

        user_2fa = Users2FAService(session).get_by_user_id(created_user.id)

        assert user_2fa

        totp = pyotp.TOTP(user_2fa.secret_key)
        valid_code = totp.now()

        response = client.post(
            f"api/v1/users/{created_user.id}/totp/verify",
            json={"user_code": valid_code, "mark_active": True},
        )

        assert response.status_code == 200

        user_2fa = Users2FAService(session).get_by_user_id(created_user.id)

        assert user_2fa and user_2fa.active

    def test_verify_incorrect_user_2fa(
        self, client: TestClient, session: Session
    ) -> None:
        created_user = create_user(session)
        CreateNewUser2FAUseCase(session).execute(created_user.id)

        user_2fa = Users2FAService(session).get_by_user_id(created_user.id)

        assert user_2fa

        response = client.post(
            f"api/v1/users/{created_user.id}/totp/verify",
            json={
                "user_code": "invalid_code",
            },
        )

        assert response.status_code == 401
