from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from tests.utils.create_provider import create_provider

login_path = "api/v1/auth/providers/login"


class TestLogin:
    def test_login(self, client: TestClient, session: Session) -> None:
        created_user = create_provider(session)

        response = client.post(
            login_path,
            json={
                "email": created_user.email,
                "password": "password",
            },
        )

        assert response.status_code == 204

    def test_login_incorrect_password(
        self, client: TestClient, session: Session
    ) -> None:
        created_user = create_provider(session)

        response = client.post(
            login_path,
            json={
                "email": created_user.email,
                "password": "incorrect_password",
            },
        )

        assert response.status_code == 401

    def test_login_non_existent_email(
        self, client: TestClient, session: Session
    ) -> None:
        create_provider(session)

        response = client.post(
            login_path,
            json={
                "email": "incorrect@email.com",
                "password": "password",
            },
        )

        assert response.status_code == 401
