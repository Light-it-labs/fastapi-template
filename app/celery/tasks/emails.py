from uuid import UUID
from app.common.clients.example_email_client import ExampleEmailClient
from app.common.exceptions.email_client_exception import EmailClientException
from app.common.schemas.pagination_schema import ListFilter
from app.common.services.emails_service import EmailService
from app.db.database_session_manager import DatabaseSessionManager
from app.main import celery


from app.core.config import get_settings
from app.users.repositories.users_repository import users_repository
from app.users.schemas.user_schema import UserInDB
from app.users.services.users_service import UsersService

settings = get_settings()


@celery.task
async def send_reminder_email() -> None:
    session_manager = DatabaseSessionManager().init()
    async with session_manager.session() as session:
        try:
            users = await UsersService(session, users_repository).list(
                ListFilter(page=1, page_size=100)
            )
            for user in users.data:
                EmailService(ExampleEmailClient()).send_user_remind_email(
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
async def send_welcome_email(user_id: UUID) -> None:
    session_manager = DatabaseSessionManager().init()
    async with session_manager.session() as session:
        try:
            user = UsersService(session, users_repository).get_by_id(user_id)
            if user:
                EmailService(ExampleEmailClient()).send_new_user_email(
                    UserInDB.model_validate(user)
                )
        finally:
            session.close()
