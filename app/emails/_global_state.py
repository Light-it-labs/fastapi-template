from app.emails.interfaces.base_email_client import BaseEmailClient
from app.emails.exceptions import GlobalEmailClientNotSetException

_client: BaseEmailClient | None = None


def set_client(client: BaseEmailClient) -> None:
    global _client
    _client = client


def get_client() -> BaseEmailClient:
    if _client is None:
        raise GlobalEmailClientNotSetException()
    return _client
