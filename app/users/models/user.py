from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from app.common.models.base_class import Base
from app.users.constants.user_constants import USER_EMAIL_MAX_LENGTH


if TYPE_CHECKING:
    from app.two_factor_authentication.models.user_2fa import Users2FA


class User(Base):
    __tablename__ = "users"

    # fields
    email: Mapped[str] = mapped_column(
        String(USER_EMAIL_MAX_LENGTH),
        unique=True,
    )
    hashed_password: Mapped[str]

    # relationships
    two_factor_authentications: Mapped[list["Users2FA"]] = relationship(
        back_populates="user",
    )
