from sqlalchemy import Column, String

from app.models.base_class import Base


class User(Base):
    __tablename__ = "users"
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
