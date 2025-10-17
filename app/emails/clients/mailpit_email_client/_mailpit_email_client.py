import requests

from app.core.config import settings
from app.common.exceptions import ExternalProviderException

from app.emails.exceptions import EmailClientException

from ..base_email_client import BaseEmailClient
from ._mailpit_email_schema import _EmailSchema, _Recipient


class MailpitEmailClient(BaseEmailClient):
    _request_timeout_in_seconds: int | None
    _mailpit_send_email_endpoint: str

    def __init__(
        self,
        request_timeout_in_seconds: int | None = 1,
        mailpit_send_email_url: str | None = None,
    ) -> None:
        super().__init__()
        self._request_timeout_in_seconds = request_timeout_in_seconds
        self._mailpit_send_email_endpoint = (
            mailpit_send_email_url
            or f"http://mailpit:{settings.FORWARD_MAILPIT_DASHBOARD_PORT}/api/v1/send"
        )

    def send_email(
        self,
        to_emails: list[str],
        html_message: str,
    ) -> None:
        email_schema = _EmailSchema(
            To=[_Recipient(Email=email) for email in to_emails],
            From=_Recipient(Email=settings.SENDER_EMAIL),
            HTML=html_message,
        )

        try:
            response = requests.post(
                self._mailpit_send_email_endpoint,
                json=email_schema.model_dump(exclude_unset=True),
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
