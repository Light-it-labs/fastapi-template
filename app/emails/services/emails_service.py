from app.core.config import settings
from app.users.schemas.user_schema import UserInDB

from app.emails._global_state import get_client
from app.emails.clients.base import BaseEmailClient
from app.emails.schema.email import Email, EmailContext
from app.emails.services.email_templates_service import (
    EmailTemplatesService,
    EmailTemplate,
)


class EmailService:
    def __init__(self, email_client: BaseEmailClient | None = None):
        self.email_client = email_client or get_client()
        self.template_service = EmailTemplatesService()

    def send_new_user_email(
        self,
        user: UserInDB,
    ) -> None:
        email = Email(
            to_emails=[user.email],
            subject="Welcome",
            html=self.template_service.render(
                EmailTemplate.WELCOME,
                name=user.email,
            ),
            context=EmailContext(
                max_retries=settings.SEND_WELCOME_EMAIL_MAX_RETRIES,
                backoff_in_seconds=settings.SEND_WELCOME_EMAIL_RETRY_BACKOFF_VALUE,
                error_message=f"Sending new user email to user {user.id} failed",
            ),
        )

        self.email_client.send_email(email)

    def send_user_remind_email(
        self,
        user: UserInDB,
    ) -> None:
        email = Email(
            to_emails=[user.email],
            subject="Welcome",
            html=self.template_service.render(
                EmailTemplate.WELCOME,
                name=user.email,
            ),
        )

        self.email_client.send_email(email)
