from abc import ABC
from typing import Any, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session


from app.common.repositories.base_repository import BaseRepository
from app.users.models.user import User

ModelType = TypeVar("ModelType", bound=Any)
TCreate = TypeVar("TCreate", bound=BaseModel)
TUpdate = TypeVar("TUpdate", bound=BaseModel)


class UsersRepository(BaseRepository[ModelType, TCreate, TUpdate], ABC):
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(self.model).filter(User.email == email).first()
