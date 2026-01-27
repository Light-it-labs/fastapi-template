from app.emails.clients.base import BaseEmailClient
from app.emails.constants.email_client import DEFAULT_ERROR_MSG
from app.emails.schema.email import Email


class CeleryTaskEmailClient(BaseEmailClient):
    def __init__(self) -> None:
        super().__init__()
        from app.celery.tasks.emails import send_email

        self.task = send_email

    def send_email(
        self,
        email: Email,
        /,
        error_message: str | None = None,
    ) -> None:
        serialized_email = email.model_dump(
            mode="json",
            exclude_unset=True,
        )

        error_message = error_message or DEFAULT_ERROR_MSG
        self.task.delay(serialized_email, error_message)
