from uuid import UUID

from pydantic import BaseModel, ConfigDict


class User2FABase(BaseModel):
    secret_key: str
    active: bool


class User2FACreate(User2FABase):
    user_id: UUID


class User2FAUpdate(User2FABase): ...


class User2FAInDB(User2FABase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


class User2FAResponse(BaseModel):
    provisioning_url: str


class VerifyUser2FARequest(BaseModel):
    user_id: UUID
    user_code: str
    mark_active: bool
