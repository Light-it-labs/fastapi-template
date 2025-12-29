from celery.schedules import crontab

from app.core.config import get_settings

settings = get_settings()


def get_transport_options() -> dict:
    if settings.BROKER_URL.startswith("sqs"):
        return {
            "region": settings.SQS_REGION or "us-east-1",
            "polling_interval": settings.SQS_POLLING_INTERVAL or 10,
        }

    return dict()


def get_celery_settings() -> dict:
    return {
        "broker_url": settings.BROKER_URL,
        "result_backend": f"db+{settings.SQLALCHEMY_DATABASE_URI}",
        "imports": ("app.celery.tasks",),
        "include": ["app.celery.tasks.emails"],
        "worker_max_tasks_per_child": 10,
        "broker_connection_retry_on_startup": True,
        "worker_send_task_events": True,
        "broker_transport_options": get_transport_options(),
        "beat_schedule_filename": ".celery/celerybeat-schedule",
        "beat_pidfile": ".celery/celerybeat.pid",
        "beat_schedule": {
            "send_reminder_email": {
                "task": "app.celery.tasks.emails.send_reminder_email",
                "schedule": crontab(minute="*/30"),
            },
        },
    }
