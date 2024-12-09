import logging
from typing import List

from app.clients.base_email_client import BaseEmailClient
from app.exceptions.email_client_exception import EmailClientException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExampleEmailClient(BaseEmailClient):
    def __init__(self) -> None:
        super().__init__(client=None)

    def send_email(
        self,
        to_emails: List[str],
        html_message: str,
        set_configuration_name: bool = False,
    ) -> None:
        # If fails, should raise an ExternalProviderException
        raise EmailClientException()
        logger.info("Sending email.")
