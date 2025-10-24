from app.common.exceptions import ExternalProviderException
from app.core.config import settings
from app.emails.clients.base import BaseEmailClient
from app.emails.schema.email import Email


class CeleryTaskEmailClient(BaseEmailClient):
    def __init__(self) -> None:
        super().__init__()
        from app.celery.tasks.emails import send_email

        self.task = send_email

    def send_email(self, /, email: Email) -> None:
        serialized_email = email.model_dump(
            mode="json",
            exclude_unset=True,
        )

        self.task.apply_async(
            args=(serialized_email,),
            retry_policy={
                "retry_errors": (ExternalProviderException,),
                "max_retries": settings.SEND_EMAIL_MAX_RETRIES,
                "interval_step": settings.SEND_EMAIL_RETRY_BACKOFF_VALUE,
            },
        )
