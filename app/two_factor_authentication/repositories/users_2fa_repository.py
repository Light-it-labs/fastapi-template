from uuid import UUID

from sqlalchemy import update
from sqlalchemy.orm import Session

from app.common.repositories.base_repository import BaseRepository
from app.two_factor_authentication.models.user_2fa import Users2FA
from app.two_factor_authentication.schemas.user_2fa_schema import User2FACreate
from app.two_factor_authentication.schemas.user_2fa_schema import User2FAUpdate


class Users2FARepository(
    BaseRepository[Users2FA, User2FACreate, User2FAUpdate],
    model=Users2FA,
):
    def get_by_user_id(
        self, session: Session, user_id: UUID
    ) -> Users2FA | None:
        return (
            session.query(self.model)
            .filter(self.model.user_id == user_id)
            .first()
        )

    def toggle_active(
        self, session: Session, user_2fa_id: UUID, active: bool
    ) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == user_2fa_id)
            .values(active=active)
        )
        session.execute(stmt)
        session.flush()


users_2fa_repository = Users2FARepository()
