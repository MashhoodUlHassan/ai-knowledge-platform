from celery import Celery


celery_app = Celery(
    "ai_knowledge_platform",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["app.workers.tasks"],
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Karachi",
    enable_utc=False,
)