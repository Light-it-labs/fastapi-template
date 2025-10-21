import requests

from app.common.exceptions import ExternalProviderException
from app.emails.interfaces.base_email_client import BaseEmailClient
from app.emails.schema.email import Email
from app.emails.exceptions import EmailClientException

from ._mailpit_email_schema import _MailpitEmailSchema


class MailpitEmailClient(BaseEmailClient):
    _mailpit_send_email_endpoint: str
    _request_timeout_in_seconds: int | None

    def __init__(
        self,
        *,
        mailpit_uri: str,
        timeout_in_seconds: int | None = None,
    ) -> None:
        super().__init__()
        self._mailpit_send_email_endpoint = f"{mailpit_uri}/send"
        self._request_timeout_in_seconds = timeout_in_seconds

    def send_email(
        self,
        /,
        email: Email,
    ) -> None:
        schema = _MailpitEmailSchema.from_email(email)

        try:
            response = requests.post(
                self._mailpit_send_email_endpoint,
                json=schema.model_dump(exclude_unset=True),
                timeout=self._request_timeout_in_seconds,
            )
        except requests.exceptions.Timeout as exc:
            message = f"Email send request timed out: {exc}"
            raise ExternalProviderException(message)
        except requests.exceptions.ConnectionError as exc:
            message = f"Connection with email client failed: {exc}"
            raise EmailClientException(message)

        if response.status_code == 200:
            return

        try:
            json = response.json()
        except requests.exceptions.JSONDecodeError as exc:
            message = (
                f"Email send request failed: couldn't decode response {exc}"
            )
            raise ExternalProviderException(message)

        message = f"Email send request failed: {json['Error']}"
        raise ExternalProviderException(message)
