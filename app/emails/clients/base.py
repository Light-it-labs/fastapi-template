import abc
import typing as t

from app.common.exceptions import ExternalProviderException
from app.emails.constants.email_client import DEFAULT_ERROR_MSG
from app.emails.schema.email import Email


class BaseEmailClient(abc.ABC):
    @abc.abstractmethod
    def send_email(
        self,
        email: Email,
        /,
        error_message: str | None = None,
    ) -> None:
        """Raises ExternalProviderException if not successful."""

    @staticmethod
    def _raise_external_provider_exception(
        error_message: str | None = None,
    ) -> t.NoReturn:
        error_message = error_message or DEFAULT_ERROR_MSG
        raise ExternalProviderException(error_message)
