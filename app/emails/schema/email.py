from pydantic import BaseModel, EmailStr, NonNegativeInt

from app.core.config import settings


class EmailContext(BaseModel):
    max_retries: NonNegativeInt = settings.SEND_EMAIL_MAX_RETRIES
    backoff_value_in_seconds: NonNegativeInt = (
        settings.SEND_EMAIL_RETRY_BACKOFF_VALUE
    )


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

    context: EmailContext | None = None
