from base.celery import celery_log_task

celery_log_task.delay(a=1,b=2)
