from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from fastapi import status

from app.auth.utils import security
from app.users.enums.user_type_enum import UserTypeEnum
from app.users.repositories.providers_repository import providers_repository
from app.users.repositories.patients_repository import patients_repository
from app.users.schemas.patient_schema import (
    CreatePatientRequest,
    PatientCreate,
    PatientResponse,
)
from app.users.services.patients_service import PatientsService
from app.users.services.providers_service import ProvidersService


class CreatePatientUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(
        self, create_patient_request: CreatePatientRequest
    ) -> PatientResponse:
        # from app.celery.tasks.emails import send_welcome_email

        patients_service = PatientsService(self.session, patients_repository)
        providers_service = ProvidersService(
            self.session, providers_repository
        )

        if (
            patients_service.get_by_email(create_patient_request.email)
            is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Patient with that email already registered.",
            )

        if (
            providers_service.get_by_id(create_patient_request.provider_id)
            is None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provider not found.",
            )

        created_patient = patients_service.create(
            PatientCreate(
                **create_patient_request.model_dump(),
                hashed_password=security.get_password_hash(
                    create_patient_request.password
                ),
                type=UserTypeEnum.PATIENT,
            )
        )

        # send_welcome_email.delay(created_user.id)  # type: ignore

        return PatientResponse(**created_patient.model_dump())
