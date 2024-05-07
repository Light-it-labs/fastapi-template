from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from tests.utils.create_user import create_user

login_path = "api/v1/auth/login"


class TestLogin:
    def test_login(self, client: TestClient, session: Session):
        created_user = create_user(session)

        response = client.post(
            login_path,
            json={
                "email": created_user.email,
                "password": "password",
            },
        )

        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_incorrect_password(self, client: TestClient, session: Session):
        created_user = create_user(session)

        response = client.post(
            login_path,
            json={
                "email": created_user.email,
                "password": "incorrect_password",
            },
        )

        assert response.status_code == 400

    def test_login_non_existent_email(self, client: TestClient, session: Session):
        create_user(session)

        response = client.post(
            login_path,
            json={
                "email": "incorrect@email.com",
                "password": "password",
            },
        )

        assert response.status_code == 400
