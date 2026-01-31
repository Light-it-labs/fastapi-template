from enum import Enum
from string import Template

from app.emails._global_state import get_client
from app.emails.clients.base import BaseEmailClient
from app.emails.schema.email import Email
from app.users.domain import User


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
        user: User,
    ) -> None:
        email = self._get_email(
            user.email,
            Paths.NEW_USER.value,
            "Welcome",
        )

        return self.email_client.send_email(email)

    def send_user_remind_email(
        self,
        user: User,
    ) -> None:
        email = self._get_email(
            user.email,
            Paths.NEW_USER.value,
            "Welcome",
        )

        return self.email_client.send_email(email)
