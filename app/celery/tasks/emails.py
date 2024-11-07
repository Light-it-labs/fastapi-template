import logging
from app.db.session import SessionLocal
from app.main import celery


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@celery.task
def send_reminder_email() -> None:
    session = SessionLocal()
    try:
        logger.info("Sending reminder email...")
    finally:
        session.close()
