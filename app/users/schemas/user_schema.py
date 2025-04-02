from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from app.users.enums.user_type_enum import UserTypeEnum


class UserBase(BaseModel):
    email: EmailStr
    hashed_password: str
    type: UserTypeEnum


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str
    type: UserTypeEnum
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    hashed_password: str | None = None


class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


class UserResponse(UserInDB):
    pass


class UserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    hashed_password: str
