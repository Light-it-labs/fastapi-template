from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import relationship

from app.users.models.user import User


class Patient(User):
    __tablename__ = "patients"

    id = Column(UUID, ForeignKey("users.id"), primary_key=True)
    provider_id = Column(UUID, ForeignKey("providers.id"), nullable=False)
    provider = relationship(
        "Provider", foreign_keys=[provider_id], back_populates="patients"
    )

    __mapper_args__ = {
        "polymorphic_identity": "patient",
    }
