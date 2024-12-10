from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    hashed_password: str | None = None


class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID


class UserResponse(UserInDB):
    pass


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str


class UserAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    hashed_password: str
