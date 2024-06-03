from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.repositories.users_repository import users_repository
from app.schemas.auth_schema import UserLogin
from app.schemas.token_schema import Token, TokenPayload
from app.services.auth_service import AuthService


class AuthUserUseCase:

    def __init__(self, session: Session):
        self.session = session

    def execute(self, login_data: UserLogin) -> Token:
        user = AuthService(self.session, users_repository).authenticate(
            email=login_data.email, password=login_data.password
        )
        return Token(access_token=create_access_token(TokenPayload(user_id=str(user.id))))
