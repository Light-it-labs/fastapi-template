from urllib.parse import quote

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.two_factor_authentication.services.users_2fa_service import (
    Users2FAService,
)

from tests.factories import UserFactory


class TestCreateNewUser2FAEndpoint:
    def test_create_new_user_2fa(
        self, client: TestClient, session: Session, user_factory: UserFactory
    ) -> None:
        user = user_factory.create()

        response = client.post(f"api/v1/users/{user.id}/totp")
        assert response.status_code == 200

        user_2fa = Users2FAService(session).get_by_user_id(user.id)
        assert user_2fa, "User2FA not created"

        assert (
            response.json()["provisioning_url"]
            == f"otpauth://totp/{settings.PROJECT_NAME}:{quote(user.email)}?secret={user_2fa.secret_key}&issuer={settings.PROJECT_NAME}"
        ), "Wrong provisioning url"
