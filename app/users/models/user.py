from unittest.mock import Base
from sqlalchemy import Column, String


class User(Base):
    __tablename__ = "users"
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
