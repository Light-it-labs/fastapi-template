from sqlalchemy.orm import Session


from fastapi import Response

from app.auth.schemas.auth_schema import UserLogin
from app.auth.services.auth_service import AuthService
from app.auth.utils.set_http_only_cookie import set_http_only_cookie
from app.users.repositories.users_repository import users_repository


class AuthUserUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(self, login_data: UserLogin, response: Response) -> None:
        patient = AuthService(self.session, users_repository).authenticate(
            login_data
        )
        set_http_only_cookie(patient.id, "access_token", response)
