from celery import Celery

# 运行
# $ celery -A tasks worker --loglevel=info
# help
# $  celery worker --help
# $ celery help
# 使用 http://supervisord.org/，让worker运行在后台

# redis://:password@hostname:port/db_number
# 默认 port 6379, using database 0.
CELERY_BROKER_URL = 'redis://127.0.0.1/0'
CELERY_RESULT_URL = 'redis://127.0.0.1/1'

# The first argument to Celery is the name of the current module.
# This is only needed so that names can be automatically generated when the tasks are defined in the __main__ module.
app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_URL)
# broker 任务队列
# backend 存储任务执行结果

@app.task
def add(x, y):
    return x + y