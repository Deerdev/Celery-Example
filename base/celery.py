from celery import Celery
from . import app_config
from base.log_task import LogTask

app = Celery("Test")

app.config_from_object(app_config)

# 老方法
# app.register_task(LogTask)

# 先注册，再调用
app.tasks.register(LogTask())
celery_log_task = LogTask()


# celery -A base worker --loglevel=info
