from app.common.schemas.common_schemas import EmailBase


class UserLogin(EmailBase):
    password: str
