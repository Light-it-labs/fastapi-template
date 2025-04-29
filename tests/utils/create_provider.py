from sqlalchemy.orm import Session

from app.auth.utils import security
from app.users.enums.user_type_enum import UserTypeEnum
from app.users.repositories.providers_repository import providers_repository
from app.users.schemas.provider_schema import ProviderCreate
from app.users.schemas.user_schema import UserInDB
from app.users.services.providers_service import ProvidersService


def create_provider(session: Session) -> UserInDB:
    hashed_password = security.get_password_hash("password")
    new_user = ProviderCreate(
        email="test0@provider.com",
        hashed_password=hashed_password,
        first_name="Provider",
        last_name="Test",
        type=UserTypeEnum.PROVIDER,
    )
    return ProvidersService(session, providers_repository).create(new_user)
