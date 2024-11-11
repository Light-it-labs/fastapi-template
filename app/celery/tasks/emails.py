from app.clients.example_email_client import ExampleEmailClient
from app.db.session import SessionLocal
from app.main import celery
from app.schemas.pagination_schema import ListFilter
from app.schemas.user_schema import UserInDB
from app.services.emails_service import EmailService
from app.services.users_service import UsersService

from app.repositories.users_repository import users_repository


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


@celery.task
def send_welcome_email(created_user: dict) -> None:
    session = SessionLocal()
    try:
        EmailService(ExampleEmailClient()).send_new_user_email(
            UserInDB.model_validate(created_user)
        )
    finally:
        session.close()
