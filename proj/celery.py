from celery import Celery

CELERY_BROKER_URL = 'redis://127.0.0.1/0'
CELERY_RESULT_URL = 'redis://127.0.0.1/1'
app = Celery('proj',
             broker=CELERY_BROKER_URL,
             backend=CELERY_RESULT_URL,
             include=['proj.tasks'])
# include:  启动时需要 import 的 work，a list of modules to import when the worker starts.
# You need to add our tasks module here so that the worker is able to find our tasks

# 设置时区
app.conf.timezone = 'Asia/Shanghai'

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)


### Route
# default queue is named celery
app.conf.update(
    task_routes = {
        'proj.tasks.add': {'queue': 'hipri'},
    },
)
# 执行时指定queue： add.apply_async((2, 2), queue='hipri')

# 指定worker处理某个、某些队列
# celery -A proj worker -Q hipri,celery



# 远程查看信息
# 查看所有worker正在处理的 task
# celery -A proj inspect active
# 只查看指定 worker (指定 host names)
# celery -A proj inspect active --destination=celery@example.com

# runtime时，修改celery
# celery -A proj control --help
# 强制所有 workers 开启/关闭 event messages (used for monitoring tasks and workers):
# celery -A proj control enable_events
# celery -A proj control disable_events

# 开启 event message 后，start the event dumper to see what the workers are doing
# celery -A proj events --dump
# celery -A proj events

# 显示在线worker
# celery -A proj status


if __name__ == '__main__':
    app.start()