from uuid import UUID

from app.common.models.base_class import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class Users2FA(Base):
    __tablename__ = "users_2fa"
    secret_key: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    active: Mapped[bool]
