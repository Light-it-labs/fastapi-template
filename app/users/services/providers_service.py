from typing import List, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from app.common.exceptions.model_not_found_exception import (
    ModelNotFoundException,
)
from app.common.schemas.pagination_schema import ListFilter
from app.users.repositories.providers_repository import ProvidersRepository
from app.users.schemas.provider_schema import (
    ProviderUpdate,
    ProviderInDB,
    ProviderCreate,
)
from app.users.services.users_service import UsersService

TInDB = TypeVar("TInDB")
TCode = TypeVar("TCode")
TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")


class ProvidersService(
    UsersService[
        ProviderInDB,
        ProviderCreate,
        ProviderUpdate,
    ]
):
    def __init__(self, session: Session, repository: ProvidersRepository):
        self.session = session
        self.repository = repository

    def create(self, create_data: ProviderCreate) -> ProviderInDB:
        created_patient = self.repository.create(self.session, create_data)
        return ProviderInDB.model_validate(created_patient)

    def update(
        self, user_id: UUID, update_data: ProviderUpdate
    ) -> ProviderInDB:
        patient_model = self.repository.get(self.session, user_id)
        if patient_model is None:
            raise ModelNotFoundException("Patient not found")

        created_patient = self.repository.update(
            self.session, patient_model, update_data
        )
        return ProviderInDB.model_validate(created_patient)

    def get_by_email(self, email: str) -> ProviderInDB | None:
        user = self.repository.get_by_email(self.session, email)
        if not user:
            return None
        return ProviderInDB.model_validate(user)

    def get_by_id(self, user_id: UUID) -> ProviderInDB | None:
        user = self.repository.get(self.session, user_id)
        if not user:
            return None
        return ProviderInDB.model_validate(user)

    def list(self, list_options: ListFilter) -> List[ProviderInDB]:
        providers = self.repository.list(self.session, list_options)
        return [
            ProviderInDB.model_validate(provider) for provider in providers
        ]
