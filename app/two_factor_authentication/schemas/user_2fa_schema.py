from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.users.schemas.user_schema import UserInDB


class User2FABase(BaseModel):
    secret_: str
    active: bool


class User2FACreate(User2FABase):
    user_id: UUID


class User2FAUpdate(User2FABase): ...


class User2FAInDB(User2FABase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user: UserInDB


class User2FAResponse(User2FAInDB):
    pass
