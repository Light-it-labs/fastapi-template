from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.users.models.user import User


class Provider(User):
    __tablename__ = "providers"

    id = Column(UUID, ForeignKey("users.id"), primary_key=True)
    patients = relationship(
        "Patient",
        back_populates="provider",
        foreign_keys="[Patient.provider_id]",
    )

    __mapper_args__ = {
        "polymorphic_identity": "provider",
    }
