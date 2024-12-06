from uuid import UUID
from app.clients.example_email_client import ExampleEmailClient
from app.db.session import SessionLocal
from app.exceptions.external_provider_error import ExternalProviderException
from app.main import celery
from app.schemas.pagination_schema import ListFilter
from app.schemas.user_schema import UserInDB
from app.services.emails_service import EmailService
from app.services.users_service import UsersService

from app.repositories.users_repository import users_repository

from app.core.config import get_settings

settings = get_settings()


@celery.task
def send_reminder_email() -> None:
    session = SessionLocal()
    try:
        users = UsersService(session, users_repository).list(
            ListFilter(page=1, page_size=100)
        )
        for user in users.data:
            EmailService(ExampleEmailClient()).send_user_remind_email(
                UserInDB.model_validate(user)
            )
    finally:
        session.close()


@celery.task(
    autoretry_for=(ExternalProviderException,),
    retry_backoff=True,
    max_retries=settings.SEND_WELCOME_EMAIL_MAX_RETRIES,
    retry_jitter=False,
)
def send_welcome_email(user_id: UUID) -> None:
    session = SessionLocal()
    try:
        user = UsersService(session, users_repository).get_by_id(user_id)
        if user:
            EmailService(ExampleEmailClient()).send_new_user_email(
                UserInDB.model_validate(user)
            )
    finally:
        session.close()
