from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models.base_class import Base


if TYPE_CHECKING:
    from app.users.models import User


class Users2FA(Base):
    __tablename__ = "users_2fa"

    # fields
    secret_key: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    active: Mapped[bool]

    # relationships
    user: Mapped["User"] = relationship(
        back_populates="two_factor_authentications",
    )
