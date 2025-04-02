from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from app.common.schemas.pagination_schema import ListFilter
from app.users.repositories.users_repository import UsersRepository

TInDB = TypeVar("TInDB")
TCode = TypeVar("TCode")
TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")


class UsersService(ABC, Generic[TInDB, TCreate, TUpdate]):
    def __init__(self, session: Session, repository: UsersRepository):
        self.session = session
        self.repository = repository

    @abstractmethod
    def create(self, create_data: TCreate) -> TInDB:
        pass

    @abstractmethod
    def update(self, user_id: UUID, update_data: TUpdate) -> TInDB:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> TInDB | None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> TInDB | None:
        pass

    @abstractmethod
    def list(self, list_options: ListFilter) -> List[TInDB]:
        pass
