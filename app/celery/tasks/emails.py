from celery import Task

from app.common.exceptions import ExternalProviderException
from app.common.schemas.pagination_schema import ListFilter
from app.core.config import settings
from app.db.session import SessionLocal
from app.emails import Email
from app.emails import EmailService
from app.emails import get_client
from app.main import celery
from app.users.schemas.user_schema import UserInDB
from app.users.services.users_service import UsersService


@celery.task
def send_reminder_email() -> None:
    service = EmailService()

    with SessionLocal() as session:
        users = UsersService(session).list(ListFilter(page=1, page_size=100))
        for user in users.data:
            service.send_user_remind_email(UserInDB.model_validate(user))


@celery.task(bind=True)
def send_email(self: Task, serialized_email: dict, error_message: str) -> None:
    email = Email(**serialized_email)
    client = get_client()

    try:
        client.send_email(email, error_message)
    except ExternalProviderException as exc:
        growth_base = settings.SEND_EMAIL_BACKOFF_GROWTH_BASE_VALUE
        retry_value = settings.SEND_EMAIL_BACKOFF_RETRY_VALUE
        max_retries = settings.SEND_EMAIL_MAX_RETRIES

        multiplier = growth_base**self.request.retries
        countdown_in_seconds = retry_value * multiplier

        raise self.retry(
            exc=exc,
            max_retries=max_retries,
            countdown=countdown_in_seconds,
        )
