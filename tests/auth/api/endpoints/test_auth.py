from fastapi.testclient import TestClient

from tests.factories import UserFactory


login_path = "api/v1/auth/login"


class TestLogin:
    def test_login(
        self, client: TestClient, user_factory: UserFactory
    ) -> None:
        user_password = "password"

        user = user_factory.create(password=user_password)

        response = client.post(
            login_path,
            json={
                "email": user.email,
                "password": user_password,
            },
        )

        assert response.status_code == 204

    def test_login_incorrect_password(
        self, client: TestClient, user_factory: UserFactory
    ) -> None:
        user = user_factory.create(password="password")

        response = client.post(
            login_path,
            json={
                "email": user.email,
                "password": "incorrect_password",
            },
        )

        assert response.status_code == 401

    def test_login_non_existent_email(
        self, client: TestClient, user_factory: UserFactory
    ) -> None:
        user_factory.create(email="test@user.com")

        response = client.post(
            login_path,
            json={
                "email": "incorrect@email.com",
                "password": "password",
            },
        )

        assert response.status_code == 401
