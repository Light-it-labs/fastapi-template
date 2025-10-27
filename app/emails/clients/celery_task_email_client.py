from app.emails.clients.base import BaseEmailClient
from app.emails.schema.email import Email, EmailContext


class CeleryTaskEmailClient(BaseEmailClient):
    def __init__(self) -> None:
        super().__init__()
        from app.celery.tasks.emails import send_email

        self.task = send_email

    def send_email(self, /, email: Email) -> None:
        if not email.context:
            email.context = EmailContext()

        serialized_email = email.model_dump(
            mode="json",
            exclude_unset=True,
        )

        self.task.delay(serialized_email)
