from uuid import UUID

from sqlalchemy.orm import Session

from app.common.repositories.base_repository import Paginator
from app.common.schemas.pagination_schema import PaginatedResponse
from app.common.schemas.pagination_schema import PaginationSettings
from app.users.models.user import User
from app.users.repositories.users_repository import UsersRepository
from app.users.repositories.users_repository import users_repository
from app.users.schemas.user_schema import UserCreate
from app.users.schemas.user_schema import UserInDB


class UsersService:
    def __init__(
        self,
        session: Session,
        repository: UsersRepository = users_repository,
    ):
        self.session = session
        self.repository = repository

    def get_by_email(self, email: str) -> UserInDB | None:
        user = self.repository.get_by_email(self.session, email.lower())
        if not user:
            return None
        return UserInDB.model_validate(user)

    def get_by_id(self, user_id: UUID) -> UserInDB | None:
        user = self.repository.get_by_id(self.session, user_id)
        if not user:
            return None
        return UserInDB.model_validate(user)

    def create_user(self, user: UserCreate) -> UserInDB:
        created_user = self.repository.create(self.session, user)
        return UserInDB.model_validate(created_user)

    def list_paginated(
        self, list_options: PaginationSettings
    ) -> PaginatedResponse[UserInDB]:
        paginator = Paginator[User](self.session, list_options)
        models = self.repository.list_all(self.session, paginator)
        schemas = [UserInDB.model_validate(user) for user in models]
        return PaginatedResponse.from_data(schemas, paginator.info)
