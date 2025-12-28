from typing import Generator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.auth.schemas.token_schema import TokenPayload
from app.auth.utils import security
from app.common.api.dependencies.get_session import get_session
from app.users.models.user import User


class ClientFactory:
    def __init__(self, app: FastAPI, session: Session):
        self._app = app
        self._session = session

        def _get_session() -> Generator:
            yield self._session

        self._app.dependency_overrides[get_session] = _get_session

    def create(self, user_to_log_in: User | None = None, /) -> TestClient:
        client = TestClient(self._app)

        if not user_to_log_in:
            return client

        # NOTE: set access token cookie to get around login endpoint limiter
        access_token = security.create_access_token(
            TokenPayload(user_id=str(user_to_log_in.id))
        )
        client.cookies = {"access_token": access_token}

        return client
