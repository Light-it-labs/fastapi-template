from uuid import UUID
from sqlalchemy.orm import Session

from app.common.exceptions.model_not_found_exception import (
    ModelNotFoundException,
)
from app.users.repositories.patients_repository import patients_repository
from app.users.schemas.patient_schema import (
    PatientResponse,
)
from app.users.services.patients_service import PatientsService


class GetPatientUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(self, patient_id: UUID) -> PatientResponse:
        patient = PatientsService(self.session, patients_repository).get_by_id(
            patient_id
        )

        if patient is None:
            raise ModelNotFoundException("Patient not found.")

        return PatientResponse(**patient.model_dump())
