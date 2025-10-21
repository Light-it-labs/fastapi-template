from .clients import BaseEmailClient
from .exceptions import GlobalEmailClientNotSetException

_client: BaseEmailClient | None = None


def set_client(client: BaseEmailClient) -> None:
    global _client
    _client = client


def get_client() -> BaseEmailClient:
    if _client is None:
        raise GlobalEmailClientNotSetException()
    return _client
