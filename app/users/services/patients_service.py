from typing import TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from app.common.exceptions.model_not_found_exception import (
    ModelNotFoundException,
)
from app.users.repositories.patients_repository import PatientsRepository
from app.users.schemas.patient_schema import (
    PatientInDB,
    PatientCreate,
    PatientUpdate,
)
from app.users.services.users_service import UsersService

TInDB = TypeVar("TInDB")
TCode = TypeVar("TCode")
TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")


class PatientsService(
    UsersService[
        PatientInDB,
        PatientCreate,
        PatientUpdate,
    ]
):
    def __init__(self, session: Session, repository: PatientsRepository):
        self.session = session
        self.repository = repository
        self.joined_loads = ["provider"]

    def create(self, create_data: PatientCreate) -> PatientInDB:
        created_patient = self.repository.create(self.session, create_data)
        return PatientInDB.model_validate(created_patient)

    def update(self, user_id: UUID, update_data: PatientUpdate) -> PatientInDB:
        patient_model = self.repository.get(self.session, user_id)
        if patient_model is None:
            raise ModelNotFoundException("Patient not found")

        created_patient = self.repository.update(
            self.session, patient_model, update_data
        )
        return PatientInDB.model_validate(created_patient)

    def get_by_email(self, email: str) -> PatientInDB | None:
        user = self.repository.get_by_email(
            self.session, email, joined_loads=self.joined_loads
        )
        if not user:
            return None
        return PatientInDB.model_validate(user)

    def get_by_id(self, user_id: UUID) -> PatientInDB | None:
        user = self.repository.get(self.session, user_id)
        if not user:
            return None
        return PatientInDB.model_validate(user)
