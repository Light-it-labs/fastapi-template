from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.auth.schemas.token_schema import EmailTokenPayload
from app.auth.utils.security import create_access_token, verify_password

from tests.factories import UserFactory


class TestResetPasswordEndpoint:
    def test_reset_password_success(
        self, client: TestClient, user_factory: UserFactory, session: Session
    ) -> None:
        user = user_factory.create()
        reset_token = create_access_token(
            EmailTokenPayload(user_email=user.email)
        )
        new_password = "MyNewSecurePassword123!"

        response = client.post(
            "/api/v1/auth/reset-password",
            headers={"token": reset_token},
            json={"password": new_password},
        )

        assert response.status_code == 204

        session.refresh(user)
        assert verify_password(new_password, user.hashed_password)

    def test_reset_password_invalid_token(
        self,
        client: TestClient,
    ) -> None:
        invalid_token = "this-is-not-a-valid-token"
        new_password = "MyNewSecurePassword123!"

        response = client.post(
            "/api/v1/auth/reset-password",
            headers={"token": invalid_token},
            json={"password": new_password},
        )

        assert response.status_code == 403
        assert "Invalid credentials" in response.json()["detail"]

    def test_reset_password_invalid_password(
        self,
        client: TestClient,
    ) -> None:
        invalid_token = "this-is-not-a-valid-token"
        new_password = "invalidpassword"

        response = client.post(
            "/api/v1/auth/reset-password",
            headers={"token": invalid_token},
            json={"password": new_password},
        )

        assert response.status_code == 422
