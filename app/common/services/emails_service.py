from enum import Enum
from string import Template


from app.common.clients.base_email_client import BaseEmailClient
from app.core.config import settings
from app.users.schemas.user_schema import UserInDB


class Paths(Enum):
    NEW_USER = "app/email_templates/welcome_email.html"


class EmailService:
    email_template = Template(
        "Subject: ${subject}\n"
        "From: FastApi <${sender_email}>\n"
        "To: <${recipient_email}>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/html\n\n"
        "${html_message}"
    )

    def __init__(self, email_client: BaseEmailClient):
        self.email_client = email_client

    def _get_email_body(
        self,
        template: str,
        subject: str,
        html_message_input: dict,
        recipient_email: str,
    ) -> str:
        with open(template, "r") as file:
            html_template_string = file.read()

        html_message = Template(html_template_string).substitute(
            **html_message_input
        )

        return self.email_template.substitute(
            subject=subject,
            html_message=html_message,
            sender_email=settings.SENDER_EMAIL,
            recipient_email=recipient_email,
        )

    def send_new_user_email(
        self,
        user: UserInDB,
    ) -> None:
        return self.email_client.send_email(
            to_emails=[user.email],
            html_message=self._get_email_body(
                Paths.NEW_USER.value,
                "Welcome",
                {},
                user.email,
            ),
        )

    def send_user_remind_email(
        self,
        user: UserInDB,
    ) -> None:
        return self.email_client.send_email(
            to_emails=[user.email],
            html_message=self._get_email_body(
                Paths.NEW_USER.value,
                "Welcome",
                {},
                user.email,
            ),
        )
