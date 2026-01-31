__all__ = (
    "CreateUserRequest",
    "UserAuth",
    "UserResponse",
)

import uuid

from pydantic import BaseModel
from pydantic import ConfigDict

from .user_types import UserEmailField
from .user_types import UserId


class UserResponse(BaseModel):
    id: UserId
    email: UserEmailField


class CreateUserRequest(BaseModel):
    email: UserEmailField
    password: str


class UserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    hashed_password: str
