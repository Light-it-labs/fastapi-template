from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str


class UserUpdate(UserBase):
    hashed_password: Optional[str] = None


class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[UUID] = None


class UserResponse(UserInDBBase):
    pass
