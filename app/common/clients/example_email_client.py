import logging
from typing import List

from app.common.clients.base_email_client import BaseEmailClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExampleEmailClient(BaseEmailClient):
    def send_email(
        self,
        to_emails: List[str],
        html_message: str,
    ) -> None:
        # If fails, should raise an ExternalProviderException
        logger.info("Sending email.")
