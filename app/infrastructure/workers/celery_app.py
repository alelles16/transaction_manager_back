from celery import Celery
import os

CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CELERY_BACKEND_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_BACKEND_URL
)

celery_app.conf.update(
    task_routes={
        "app.infrastructure.workers.tasks.*": {"queue": "default"},
    },
    task_track_started=True,
    task_time_limit=300,
)
