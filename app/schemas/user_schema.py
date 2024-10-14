from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr | None = None


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str


class UserUpdate(UserBase):
    hashed_password: str | None = None


class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID | None = None


class UserResponse(UserInDBBase):
    pass
