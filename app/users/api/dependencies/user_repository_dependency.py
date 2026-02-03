__all__ = (
    "get_user_repository",
    "UserRepositoryDependency",
)

import typing as t

import fastapi

from app.common.api.dependencies import SessionDependency
from app.users.domain import UserRepository
from app.users.infrastructure import SQLAlchemyUserRepository


def get_user_repository(session: SessionDependency) -> UserRepository:
    return SQLAlchemyUserRepository(session)


UserRepositoryDependency = t.Annotated[
    UserRepository,
    fastapi.Depends(get_user_repository),
]
