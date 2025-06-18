from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String

from app.common.models.base_class import Base


class User(Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str]
