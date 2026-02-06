from typing import Generator

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import RootTransaction, event
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.main import app

from tests.factories import ClientFactory, UserFactory


TEST_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI


@pytest.fixture()
def session() -> Generator:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(session: Session, transaction: RootTransaction) -> None:
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client_factory(session: Session) -> ClientFactory:
    return ClientFactory(app, session)


@pytest.fixture()
def client(client_factory: ClientFactory) -> TestClient:
    return client_factory.create()


@pytest.fixture()
def user_factory(session: Session) -> UserFactory:
    return UserFactory(session)
