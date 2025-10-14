from typing import Any, Final
from uuid import UUID

from fastapi import Response
from fastapi.testclient import TestClient
import pyotp
from sqlalchemy.orm import Session

from app.two_factor_authentication.models import Users2FA

from tests.factories import UserFactory


class TestVerifyUser2FAEndpoint:
    URL: Final = "api/v1/users/{user_id}/totp/verify"

    def test_verify_correct_user_2fa(
        self,
        client: TestClient,
        user_factory: UserFactory,
    ) -> None:
        user = user_factory.create(with_2fa=True)
        user_2fa = user.two_factor_authentications[0]

        totp = pyotp.TOTP(user_2fa.secret_key)
        valid_code = totp.now()

        response = self._post(client, user.id, valid_code)
        assert response.status_code == 200

    def test_verify_correct_user_2fa_and_mark_active(
        self,
        client: TestClient,
        session: Session,
        user_factory: UserFactory,
    ) -> None:
        user = user_factory.create(with_2fa=True)
        user_2fa = user.two_factor_authentications[0]

        totp = pyotp.TOTP(user_2fa.secret_key)
        valid_code = totp.now()

        response = self._post(client, user.id, valid_code, mark_active=True)
        assert response.status_code == 200

        assert (user_2fa := session.get(Users2FA, user_2fa.id))
        assert user_2fa.active

    def test_verify_incorrect_user_2fa(
        self,
        client: TestClient,
        user_factory: UserFactory,
    ) -> None:
        user = user_factory.create(with_2fa=True)

        response = self._post(client, user.id, "invalid_code")
        assert response.status_code == 401

    def _post(
        self,
        client: TestClient,
        user_id: UUID,
        code: str,
        mark_active: bool | None = None,
    ) -> Response:
        url = self.URL.format(user_id=user_id)
        json: dict[str, Any] = {"user_code": code}
        if mark_active is not None:
            json["mark_active"] = mark_active

        return client.post(url, json=json)
