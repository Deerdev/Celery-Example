from base.celery import celery_log_task
from base.log_task import LogTask

result = celery_log_task.delay(a=1, b=2).get()
print(result)

# 直接调用 class
# LogTask().delay(a=1, b=2)
