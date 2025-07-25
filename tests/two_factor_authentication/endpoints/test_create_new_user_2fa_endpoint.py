from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.two_factor_authentication.services.users_2fa_service import (
    Users2FAService,
)
from tests.utils.create_user import create_user
from urllib.parse import quote

settings = get_settings()


class TestCreateNewUser2FAEndpoint:
    def test_create_new_user_2fa(
        self, client: TestClient, session: Session
    ) -> None:
        created_user = create_user(session)

        response = client.post(
            f"api/v1/users/{created_user.id}/totp",
        )
        user_2fa = Users2FAService(session).get_by_user_id(created_user.id)

        assert response.status_code == 200

        assert user_2fa

        assert (
            response.json()["provisioning_url"]
            == f"otpauth://totp/{settings.PROJECT_NAME}:{quote(created_user.email)}?secret={user_2fa.secret_key}&issuer={settings.PROJECT_NAME}"
        )
