import pytest
from sqlalchemy import event
from fastapi.testclient import TestClient

from app.api.dependencies.get_db import get_db
from app.core.config import get_settings
from app.db.session import engine, SessionLocal
from app.main import app

settings = get_settings()
TEST_DATABASE_URI = settings.SQLALCHEMY_DATABASE_URI


@pytest.fixture()
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(session):
    # Use the same session as the session fixture
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client
