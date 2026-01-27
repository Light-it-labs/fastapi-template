from typing import ClassVar

from app.common.clients.base_request_client import BaseRequestClient
from app.core.config import settings
from app.emails.clients.base import BaseEmailClient
from app.emails.schema.email import Email

from ._mailpit_email_schema import _MailpitEmailSchema


class MailpitEmailClient(BaseEmailClient, BaseRequestClient):
    _SEND_EMAIL_ENDPOINT: ClassVar[str] = "/send"

    def __init__(
        self,
        *,
        mailpit_uri: str | None = None,
    ) -> None:
        super().__init__()
        self.base_url = mailpit_uri or settings.MAILPIT_URI

    def send_email(
        self,
        email: Email,
        /,
        error_message: str | None = None,
    ) -> None:
        schema = _MailpitEmailSchema.from_email(email)

        response = self._make_request(
            endpoint=self._SEND_EMAIL_ENDPOINT,
            method="POST",
            json=schema.model_dump(exclude_unset=True),
        )

        if not response:
            self._raise_external_provider_exception(error_message)
