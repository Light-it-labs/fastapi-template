from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.exceptions.model_not_found_exception import ModelNotFoundException
from app.repositories.users_repository import UsersRepository
from app.schemas.user_schema import UserInDBBase


class AuthService:
    def __init__(self, session: Session, repository: UsersRepository):
        self.session = session
        self.repository = repository

    def authenticate(self, email: str, password: str) -> UserInDBBase:
        user = self.repository.get_by_email(self.session, email=email)
        if not user:
            raise ModelNotFoundException()
        if not verify_password(password, str(user.hashed_password)):
            raise InvalidCredentialsException()
        return UserInDBBase.model_validate(user)
