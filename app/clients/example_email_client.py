from typing import List

from app.clients.base_email_client import BaseEmailClient
from app.celery.tasks.emails import send_welcome_email


class ExampleEmailClient(BaseEmailClient):
    def __init__(self) -> None:
        super().__init__(client=None)

    def send_email(
        self,
        to_emails: List[str],
        html_message: str,
        set_configuration_name: bool = False,
    ) -> None:
        for email in to_emails:
            send_welcome_email.delay(email)  # type: ignore
