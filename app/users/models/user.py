from sqlalchemy import Column, String

from app.common.models.base_class import Base

from app.users.constants.user_constants import USER_EMAIL_MAX_LENGTH


class User(Base):
    __tablename__ = "users"
    email = Column(String(USER_EMAIL_MAX_LENGTH), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
