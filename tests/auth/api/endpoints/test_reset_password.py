from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.auth.schemas.token_schema import EmailTokenPayload
from app.auth.utils.security import create_access_token, verify_password
from app.users.models.user import User
from tests.utils.create_user import create_user


class TestResetPasswordEndpoint:
    def test_reset_password_success(
        self, client: TestClient, session: Session
    ) -> None:
        created_user = create_user(session)
        reset_token = create_access_token(
            EmailTokenPayload(user_email=created_user.email)
        )
        new_password = "MyNewSecurePassword123!"

        response = client.post(
            "/api/v1/auth/reset-password",
            headers={"token": reset_token},
            json={"password": new_password},
        )

        assert response.status_code == 204

        user = session.query(User).filter(User.id == created_user.id).first()
        assert user and verify_password(new_password, user.hashed_password)

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
