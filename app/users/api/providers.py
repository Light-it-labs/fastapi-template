from uuid import UUID
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from app.common.exceptions.model_not_found_exception import (
    ModelNotFoundException,
)
from app.users.schemas.patient_schema import (
    CreatePatientRequest,
    PatientResponse,
)
from app.users.api.dependencies.get_current_provider import CurrentProvider
from app.common.api.dependencies.get_session import SessionDependency
from app.users.schemas.provider_schema import ProviderResponse
from app.users.use_cases.create_patient_use_case import CreatePatientUseCase
from app.users.use_cases.get_patient_use_case import GetPatientUseCase

router = APIRouter()


@router.get("/current", status_code=status.HTTP_200_OK)
def get_current_provider(
    current_provider: CurrentProvider,
) -> ProviderResponse:
    return ProviderResponse.model_validate(current_provider)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_patient(
    session: SessionDependency,
    create_patient_request: CreatePatientRequest,
) -> PatientResponse:
    return CreatePatientUseCase(session).execute(create_patient_request)


@router.get("/{patient_id}", status_code=status.HTTP_200_OK)
def get_patient(
    session: SessionDependency,
    patient_id: UUID,
) -> PatientResponse:
    try:
        return GetPatientUseCase(session).execute(patient_id)
    except ModelNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )
