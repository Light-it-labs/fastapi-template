__all__ = ("User",)

import datetime as dt

import pydantic

from app.common.domain import Entity

from .user_types import UserEmailField
from .user_types import UserId


class User(Entity):
    id: UserId
    created_at: dt.datetime
    updated_at: dt.datetime

    email: UserEmailField
    hashed_password: str

    class CreateDto(pydantic.BaseModel):
        email: UserEmailField
        hashed_password: str

    class UpdateDto(pydantic.BaseModel):
        email: UserEmailField | None = None
        hashed_password: str | None = None
