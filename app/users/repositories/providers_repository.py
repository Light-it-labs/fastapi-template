from app.users.models import Provider
from app.users.repositories.users_repository import UsersRepository
from app.users.schemas.provider_schema import ProviderCreate, ProviderUpdate


class ProvidersRepository(
    UsersRepository[Provider, ProviderCreate, ProviderUpdate]
):
    pass


providers_repository = ProvidersRepository(Provider)
