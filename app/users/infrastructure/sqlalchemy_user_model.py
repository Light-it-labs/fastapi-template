__all__ = ("SQLAlchemyUserModel",)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import String

import app.users.domain as user_domain
from app.common.infrastructure import BaseSQLAlchemyModel


class SQLAlchemyUserModel(BaseSQLAlchemyModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(user_domain.USER_EMAIL_MAX_LENGTH),
        unique=True,
    )
    hashed_password: Mapped[str]
