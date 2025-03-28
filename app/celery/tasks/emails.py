from uuid import UUID
from app.common.clients.example_email_client import ExampleEmailClient
from app.common.exceptions.email_client_exception import EmailClientException
from app.common.schemas.pagination_schema import ListFilter
from app.common.services.emails_service import EmailService
from app.db.session import SessionLocal
from app.main import celery


from app.core.config import get_settings
from app.users.repositories.patients_repository import patients_repository
from app.users.schemas.patient_schema import PatientInDB
from app.users.schemas.user_schema import UserInDB
from app.users.services.patients_service import PatientsService

settings = get_settings()


@celery.task
def send_reminder_email() -> None:
    session = SessionLocal()
    try:
        patients = PatientsService(session, patients_repository).list(
            ListFilter(page=1, page_size=100)
        )
        for patient in patients.data:
            EmailService(ExampleEmailClient()).send_user_remind_email(
                UserInDB.model_validate(patient)
            )
    finally:
        session.close()


@celery.task(
    autoretry_for=(EmailClientException,),
    retry_backoff=settings.SEND_WELCOME_EMAIL_RETRY_BACKOFF_VALUE,
    max_retries=settings.SEND_WELCOME_EMAIL_MAX_RETRIES,
    retry_jitter=False,
)
def send_welcome_email(patient_id: UUID) -> None:
    session = SessionLocal()
    try:
        patient = PatientsService(session, patients_repository).get_by_id(
            patient_id
        )
        if patient:
            EmailService(ExampleEmailClient()).send_new_user_email(
                PatientInDB.model_validate(patient)
            )
    finally:
        session.close()
