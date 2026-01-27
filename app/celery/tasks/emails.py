from typing import Final

from celery import Task

from app.common.exceptions import ExternalProviderException
from app.common.schemas.pagination_schema import ListFilter
from app.db.session import SessionLocal
from app.emails import Email
from app.emails import EmailService
from app.emails import get_client
from app.main import celery
from app.users.schemas.user_schema import UserInDB
from app.users.services.users_service import UsersService

BACKOFF_EXPONENTIAL_GROWTH_BASE: Final[int] = 2


@celery.task
def send_reminder_email() -> None:
    service = EmailService()

    with SessionLocal() as session:
        users = UsersService(session).list(ListFilter(page=1, page_size=100))
        for user in users.data:
            service.send_user_remind_email(UserInDB.model_validate(user))


@celery.task(bind=True)
def send_email(self: Task, serialized_email: dict) -> None:
    email = Email(**serialized_email)
    client = get_client()

    try:
        client.send_email(email)
    except ExternalProviderException as exc:
        if not email.context:
            raise

        multiplier = BACKOFF_EXPONENTIAL_GROWTH_BASE**self.request.retries
        countdown_in_seconds = email.context.backoff_in_seconds * multiplier

        raise self.retry(
            exc=exc,
            max_retries=email.context.max_retries,
            countdown=countdown_in_seconds,
        )
