from app.users.schemas.user_schema import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserInDB,
)


class ProviderBase(UserBase):
    pass


class ProviderCreate(UserCreate):
    pass


class ProviderUpdate(UserUpdate):
    pass


class ProviderInDB(UserInDB):
    pass


class ProviderResponse(ProviderInDB):
    pass
