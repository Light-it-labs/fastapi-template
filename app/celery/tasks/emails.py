from app.common.schemas.pagination_schema import ListFilter
from app.emails import Email, EmailService, get_client
from app.db.session import SessionLocal
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


@celery.task
def send_email(serialized_email: dict) -> None:
    email = Email(**serialized_email)
    client = get_client()
    client.send_email(email)
