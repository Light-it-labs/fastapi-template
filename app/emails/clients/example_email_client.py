import logging

from app.emails.clients.base import BaseEmailClient
from app.emails.schema.email import Email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExampleEmailClient(BaseEmailClient):
    def send_email(
        self,
        email: Email,
        /,
        error_message: str | None = None,
    ) -> None:
        logger.info("Sending email from example.")
