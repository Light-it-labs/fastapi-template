from pydantic import BaseModel, field_validator
from app.auth.utils.validate_password import validate_password
from app.common.schemas.common_schemas import EmailBase


class UserLogin(EmailBase):
    password: str


class PasswordResetRequest(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        return validate_password(v)
