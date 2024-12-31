from sqlalchemy.orm import Session

from app.auth.schemas.auth_schema import UserLogin
from app.common.exceptions.model_not_found_exception import (
    ModelNotFoundException,
)
from app.auth.utils.security import verify_password
from app.auth.exceptions.invalid_credentials_exception import (
    InvalidCredentialsException,
)
from app.users.repositories.users_repository import UsersRepository
from app.users.schemas.user_schema import UserAuth


class AuthService:
    def __init__(self, session: Session, repository: UsersRepository):
        self.session = session
        self.repository = repository

    def authenticate(self, login_data: UserLogin) -> UserAuth:
        user = self.repository.get_by_email(
            self.session, email=login_data.email
        )
        if not user:
            raise ModelNotFoundException()
        user_schema = UserAuth.model_validate(user)
        if not verify_password(
            login_data.password, user_schema.hashed_password
        ):
            raise InvalidCredentialsException()
        return user_schema
