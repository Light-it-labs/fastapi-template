from sqlalchemy.orm import Session

from app.repositories.users_repository import users_repository
from app.schemas.auth_schema import UserLogin
from app.services.auth_service import AuthService

from fastapi import Response

from app.utils.set_http_only_cookie import set_http_only_cookie


class AuthUserUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(self, login_data: UserLogin, response: Response) -> None:
        patient = AuthService(self.session, users_repository).authenticate(
            login_data
        )
        set_http_only_cookie(patient.id, "access_token", response)
