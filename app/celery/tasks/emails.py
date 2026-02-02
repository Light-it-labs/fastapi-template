from app.common.domain import Paginator
from app.core.config import settings
from app.db.session import SessionLocal
from app.emails.exceptions.email_client_exception import EmailClientException
from app.emails.services.emails_service import EmailService
from app.main import celery
from app.users.domain import UserId
from app.users.infrastructure import SQLAlchemyUserRepository


@celery.task
def send_reminder_email() -> None:
    email_service = EmailService()

    with SessionLocal() as session:
        user_repository = SQLAlchemyUserRepository(session)
        users = user_repository.where(Paginator(page=1, page_size=100))
        for user in users:
            email_service.send_user_remind_email(user)


@celery.task(
    autoretry_for=(EmailClientException,),
    retry_backoff=settings.SEND_WELCOME_EMAIL_RETRY_BACKOFF_VALUE,
    max_retries=settings.SEND_WELCOME_EMAIL_MAX_RETRIES,
    retry_jitter=False,
)
def send_welcome_email(user_id: UserId) -> None:
    with SessionLocal() as session:
        user = SQLAlchemyUserRepository(session).find_or_fail(user_id)
        EmailService().send_new_user_email(user)
