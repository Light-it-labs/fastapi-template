__all__ = (
    "UserEmailField",
    "UserId",
)

import typing as t
import uuid

import pydantic

from .user_constants import USER_EMAIL_MAX_LENGTH

UserId = t.NewType("UserId", uuid.UUID)

UserEmailField = t.Annotated[
    pydantic.EmailStr,
    pydantic.Field(max_length=USER_EMAIL_MAX_LENGTH),
    pydantic.AfterValidator(lambda s: s.lower()),
]
