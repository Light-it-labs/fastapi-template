from uuid import UUID

from app.common.schemas.pagination_schema import PaginationSettings
from app.core.config import get_settings
from app.db.session import SessionLocal
from app.emails.exceptions.email_client_exception import EmailClientException
from app.emails.services.emails_service import EmailService
from app.main import celery
from app.users.schemas.user_schema import UserInDB
from app.users.services.users_service import UsersService

settings = get_settings()


@celery.task
def send_reminder_email() -> None:
    session = SessionLocal()
    try:
        users = UsersService(session).list_paginated(
            PaginationSettings(page=1, page_size=100)
        )
        for user in users.data:
            EmailService().send_user_remind_email(
                UserInDB.model_validate(user)
            )
    finally:
        session.close()


@celery.task(
    autoretry_for=(EmailClientException,),
    retry_backoff=settings.SEND_WELCOME_EMAIL_RETRY_BACKOFF_VALUE,
    max_retries=settings.SEND_WELCOME_EMAIL_MAX_RETRIES,
    retry_jitter=False,
)
def send_welcome_email(user_id: UUID) -> None:
    session = SessionLocal()
    try:
        user = UsersService(session).get_by_id(user_id)
        if user:
            EmailService().send_new_user_email(UserInDB.model_validate(user))
    finally:
        session.close()
