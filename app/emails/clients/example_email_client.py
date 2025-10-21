import logging

from app.emails.interfaces.base_email_client import BaseEmailClient
from app.emails.schema.email import Email


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExampleEmailClient(BaseEmailClient):
    def send_email(self, /, email: Email) -> None:
        # If fails, should raise an ExternalProviderException
        logger.info("Sending email from example.")
