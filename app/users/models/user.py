from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String

from app.common.models.base_class import Base

from app.users.constants.user_constants import USER_EMAIL_MAX_LENGTH


class User(Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(
        String(USER_EMAIL_MAX_LENGTH), unique=True
    )
    hashed_password: Mapped[str]
