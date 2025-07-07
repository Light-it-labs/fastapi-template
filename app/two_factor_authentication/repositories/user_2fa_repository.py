from uuid import UUID
from sqlalchemy.orm import Session


from app.common.repositories.base_repository import BaseRepository
from app.two_factor_authentication.models.user_2fa import Users2FA
from app.two_factor_authentication.schemas.user_2fa_schema import (
    User2FACreate,
    User2FAUpdate,
)


class Users2FARepository(
    BaseRepository[Users2FA, User2FACreate, User2FAUpdate]
):
    def get_by_user_id(self, db: Session, user_id: UUID) -> Users2FA | None:
        return db.query(self.model).filter(Users2FA.user_id == user_id).first()


users_2fa_repository = Users2FARepository(Users2FA)
