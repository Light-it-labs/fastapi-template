from uuid import UUID

from sqlalchemy.orm import Session

from app.two_factor_authentication.repositories.users_2fa_repository import (
    users_2fa_repository,
)
from app.two_factor_authentication.repositories.users_2fa_repository import (
    Users2FARepository,
)
from app.two_factor_authentication.schemas.user_2fa_schema import (
    User2FACreate,
    User2FAInDB,
)


class Users2FAService:
    def __init__(
        self,
        session: Session,
        repository: Users2FARepository = users_2fa_repository,
    ):
        self.session = session
        self.repository = repository

    def get_by_user_id(self, user_id: UUID) -> User2FAInDB | None:
        user_2fa = self.repository.get_by_user_id(self.session, user_id)
        if not user_2fa:
            return None
        return User2FAInDB.model_validate(user_2fa)

    def create_user_2fa(self, user_2fa: User2FACreate) -> User2FAInDB:
        created_user_2fa = self.repository.create(self.session, user_2fa)
        return User2FAInDB.model_validate(created_user_2fa)

    def toggle_active(self, user_2fa_id: UUID, active: bool) -> None:
        self.repository.toggle_active(self.session, user_2fa_id, active)
