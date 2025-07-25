from uuid import UUID
from sqlalchemy.orm import Session
import pyotp
from app.common.exceptions.model_not_created_exception import (
    ModelNotCreatedException,
)
from app.common.exceptions.model_not_found_exception import (
    ModelNotFoundException,
)
from app.core.config import get_settings
from app.two_factor_authentication.schemas.user_2fa_schema import (
    User2FACreate,
    User2FAResponse,
)
from app.two_factor_authentication.services.users_2fa_service import (
    Users2FAService,
)
from app.users.repositories.users_repository import users_repository
from app.users.services.users_service import UsersService

settings = get_settings()


class CreateNewUser2FAUseCase:
    def __init__(self, session: Session):
        self.session = session
        self.users_service = UsersService(self.session, users_repository)
        self.users_2fa_service = Users2FAService(self.session)

    def execute(self, user_id: UUID) -> User2FAResponse:
        secret_key = pyotp.random_base32()

        user = self.users_service.get_by_id(user_id)
        if not user:
            raise ModelNotFoundException("User not found")

        user_2fa = self.users_2fa_service.create_user_2fa(
            User2FACreate(secret_key=secret_key, active=False, user_id=user.id)
        )

        if not user_2fa:
            raise ModelNotCreatedException(
                "There was an error creating users 2fa"
            )

        provisioning_uri = pyotp.totp.TOTP(secret_key).provisioning_uri(
            name=user.email, issuer_name=settings.PROJECT_NAME
        )
        return User2FAResponse(provisioning_url=provisioning_uri)
