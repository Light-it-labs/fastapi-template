from app.schemas.common_schemas import EmailBase


class UserLogin(EmailBase):
    password: str
