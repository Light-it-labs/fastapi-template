from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.users_repository import UsersRepository
from app.schemas.user_schema import UserCreate, UserInDB


class UsersService:
    def __init__(self, session: Session, repository: UsersRepository):
        self.session = session
        self.repository = repository

    def get_by_email(self, email: str) -> UserInDB | None:
        user = self.repository.get_by_email(self.session, email)
        if not user:
            return None
        return UserInDB.model_validate(user)

    def get_by_id(self, user_id: UUID) -> UserInDB | None:
        user = self.repository.get(self.session, user_id)
        if not user:
            return None
        return UserInDB.model_validate(user)

    def create_user(self, user: UserCreate) -> UserInDB:
        created_user = self.repository.create(self.session, user)
        return UserInDB.model_validate(created_user)
