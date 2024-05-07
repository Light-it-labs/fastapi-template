from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.repositories.users_repository import UsersRepository
from app.schemas.user_schema import UserInDBBase


class AuthService:
    def __init__(self, session: Session, repository: UsersRepository):
        self.session = session
        self.repository = repository

    def authenticate(self, email: str, password: str) -> UserInDBBase | None:
        user = self.repository.get_by_email(self.session, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return UserInDBBase.model_validate(user)
