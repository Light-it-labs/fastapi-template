from sqlalchemy.orm import Session


from app.auth.utils import security
from app.users.enums.user_type_enum import UserTypeEnum
from app.users.repositories.patients_repository import patients_repository
from app.users.repositories.providers_repository import providers_repository
from app.users.schemas.patient_schema import PatientCreate
from app.users.schemas.provider_schema import ProviderCreate
from app.users.services.providers_service import ProvidersService
from app.users.services.patients_service import PatientsService

from faker import Faker

fake = Faker()


class UsersSeeder:
    @staticmethod
    def run(db: Session) -> None:
        hashed_password = security.get_password_hash("password")
        provider = ProvidersService(db, providers_repository).create(
            ProviderCreate(
                email="test0@provider.com",
                hashed_password=hashed_password,
                first_name="Provider",
                last_name="Test",
                type=UserTypeEnum.PROVIDER,
            )
        )

        patients_service = PatientsService(db, patients_repository)
        for _ in range(1, 10):
            patients_service.create(
                PatientCreate(
                    email=fake.email(),
                    hashed_password=hashed_password,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    type=UserTypeEnum.PATIENT,
                    provider_id=provider.id,
                )
            )
        db.commit()
