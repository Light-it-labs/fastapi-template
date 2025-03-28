from fastapi import APIRouter, status

from app.users.schemas.patient_schema import (
    CreatePatientRequest,
    PatientResponse,
)
from app.users.api.dependencies.get_current_provider import CurrentProvider
from app.common.api.dependencies.get_session import SessionDependency
from app.users.use_cases.create_patient_use_case import CreatePatientUseCase

router = APIRouter()


@router.get("/current", status_code=status.HTTP_200_OK)
def get_current_patient(
    current_user: CurrentProvider,
) -> PatientResponse:
    return PatientResponse.model_validate(current_user)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_patient(
    session: SessionDependency,
    create_patient_request: CreatePatientRequest,
) -> PatientResponse:
    return CreatePatientUseCase(session).execute(create_patient_request)
