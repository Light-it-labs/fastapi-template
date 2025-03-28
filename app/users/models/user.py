from sqlalchemy import Column, String

from app.common.models.base_class import Base


class User(Base):
    __tablename__ = "users"  # type: ignore

    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    type = Column(String, nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "users",
        "polymorphic_on": "type",
    }
