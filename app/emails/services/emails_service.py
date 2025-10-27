from enum import Enum
from string import Template

from app.core.config import settings
from app.users.schemas.user_schema import UserInDB
from app.emails.clients.base import BaseEmailClient
from app.emails.schema.email import Email, EmailContext
from app.emails._global_state import get_client


class Paths(Enum):
    NEW_USER = "app/emails/templates/welcome_email.html"


class EmailService:
    def __init__(self, email_client: BaseEmailClient | None = None):
        self.email_client = email_client or get_client()

    def _get_email(
        self,
        recipient_email: str,
        template: str,
        subject: str,
        html_message_input: dict | None = None,
    ) -> Email:
        with open(template, "r") as file:
            html_template_string = file.read()

        html_message_input = html_message_input or {}
        html = Template(html_template_string).substitute(**html_message_input)

        return Email(
            to_emails=[recipient_email],
            subject=subject,
            html=html,
        )

    def send_new_user_email(
        self,
        user: UserInDB,
    ) -> None:
        email = self._get_email(
            user.email,
            Paths.NEW_USER.value,
            "Welcome",
        )

        email.context = EmailContext(
            max_retries=settings.SEND_WELCOME_EMAIL_MAX_RETRIES,
            backoff_in_seconds=settings.SEND_WELCOME_EMAIL_RETRY_BACKOFF_VALUE,
            error_message=f"Sending new user email to user {user.id} failed",
        )

        self.email_client.send_email(email)

    def send_user_remind_email(
        self,
        user: UserInDB,
    ) -> None:
        email = self._get_email(
            user.email,
            Paths.NEW_USER.value,
            "Welcome",
        )

        self.email_client.send_email(email)
