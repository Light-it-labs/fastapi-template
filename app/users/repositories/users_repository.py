from abc import ABC
from typing import Any, TypeVar, List
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload

from app.common.repositories.base_repository import BaseRepository
from app.users.models.user import User

ModelType = TypeVar("ModelType", bound=Any)
TCreate = TypeVar("TCreate", bound=BaseModel)
TUpdate = TypeVar("TUpdate", bound=BaseModel)


class UsersRepository(BaseRepository[ModelType, TCreate, TUpdate], ABC):
    def get_by_email(
        self, db: Session, email: str, joined_loads: List[str] | None = None
    ) -> User | None:
        query = db.query(self.model).filter(User.email == email)

        if joined_loads:
            for relation in joined_loads:
                query = query.options(
                    joinedload(getattr(self.model, relation))
                )

        return query.first()
