from pydantic import BaseModel, EmailStr

from app.core.config import settings


class Email(BaseModel):
    from_email: EmailStr = settings.SENDER_EMAIL
    from_name: str = "FastApi"

    to_emails: list[EmailStr]
    cc_emails: list[EmailStr] = []
    bcc_emails: list[EmailStr] = []

    subject: str | None = None
    html: str = ""

    headers: dict[str, str] | None = {
        "MIME-Version": "1.0",
        "Content-Type": "text/html",
    }
