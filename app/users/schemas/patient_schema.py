from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, EmailStr, StringConstraints

from app.users.schemas.provider_schema import ProviderInDB
from app.users.schemas.user_schema import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserInDB,
)


class PatientBase(UserBase):
    provider_id: UUID


class PatientCreate(UserCreate):
    provider_id: UUID


class PatientUpdate(UserUpdate):
    pass


class PatientInDB(UserInDB, PatientBase):
    provider_id: UUID
    provider: ProviderInDB


class PatientResponse(PatientInDB):
    pass


class CreatePatientRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Annotated[str, StringConstraints(max_length=30)]
    last_name: Annotated[str, StringConstraints(max_length=30)]
    provider_id: UUID
