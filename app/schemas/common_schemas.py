from pydantic import BaseModel, EmailStr, field_validator


class EmailBase(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def lower_email(cls, v: str) -> str:
        return v.lower()
