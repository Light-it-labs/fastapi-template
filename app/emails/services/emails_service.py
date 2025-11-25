from app import templates
from app.core.config import settings
from app.users.schemas.user_schema import UserInDB

from app.emails._global_state import get_client
from app.emails.clients.base import BaseEmailClient
from app.emails.schema.email import Email, EmailContext


# TODO: the service will not be coupled to different modules once the
# rendering of the notification is refactored out to a Notification class.
# Then those implementation details will be contained on each module.
class EmailService:
    def __init__(self, email_client: BaseEmailClient | None = None):
        self.email_client = email_client or get_client()
        self.template_service = templates.TemplatesService()

    def send_new_user_email(
        self,
        user: UserInDB,
    ) -> None:
        from app.users.schemas.templates import NewUserTemplate

        template = NewUserTemplate(name=user.email)

        email = Email(
            to_emails=[user.email],
            subject="Welcome",
            html=self.template_service.render(template),
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
        from app.users.schemas.templates import NewUserTemplate

        template = NewUserTemplate(name=user.email)

        email = Email(
            to_emails=[user.email],
            subject="Welcome",
            html=self.template_service.render(template),
        )

        self.email_client.send_email(email)
