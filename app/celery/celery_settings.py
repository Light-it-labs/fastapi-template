from celery.schedules import crontab

from app.core.config import get_settings

settings = get_settings()


def get_celery_settings() -> dict:
    return {
        "broker_url": settings.rabbitmq_url,
        "result_backend": f"db+{settings.SQLALCHEMY_DATABASE_URI}",
        "imports": ("app.celery.tasks",),
        "include": ["app.celery.tasks.emails"],
        "worker_max_tasks_per_child": 10,
        "broker_connection_retry_on_startup": True,
        "worker_send_task_events": True,
        "beat_schedule": {
            "send_reminder_email": {
                "task": "app.celery.tasks.emails.send_reminder_email",
                "schedule": crontab(minute="*/30"),
            },
        },
    }
