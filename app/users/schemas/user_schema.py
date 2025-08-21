from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.users.constants.user_constants import USER_EMAIL_MAX_LENGTH

_UserEmailField = Field(max_length=USER_EMAIL_MAX_LENGTH)


class UserBase(BaseModel):
    email: Annotated[EmailStr, _UserEmailField]


class UserCreate(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    email: Annotated[EmailStr | None, _UserEmailField] = None
    hashed_password: str | None = None


class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


class UserResponse(UserInDB):
    pass


class CreateUserRequest(UserBase):
    password: str


class UserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    hashed_password: str
