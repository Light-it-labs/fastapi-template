from math import ceil
from sqlalchemy.orm import Session

from app.common.schemas.pagination_schema import ListFilter, ListResponse
from app.users.repositories.patients_repository import patients_repository
from app.users.services.patients_service import PatientsService


class ListPatientUseCase:
    def __init__(self, session: Session):
        self.session = session

    def execute(self, list_filter: ListFilter) -> ListResponse:
        patients = PatientsService(self.session, patients_repository).list(
            list_options=list_filter
        )

        return ListResponse(
            data=patients,
            page=list_filter.page,
            page_size=list_filter.page_size,
            total=len(patients),
            total_pages=ceil(len(patients) / list_filter.page_size),
        )
