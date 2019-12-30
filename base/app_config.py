# https://docs.celeryproject.org/en/latest/userguide/configuration.html#example-configuration-file

import re


broker_url = "redis://127.0.0.1/0"
result_backend = "redis://127.0.0.1/1"

task_ignore_result = True
task_serializer = 'json'
result_serializer = 'json'
# 并发处理
worker_concurrency = 4
# 禁用预处理
worker_prefetch_multiplier = 1

timezone = "Asia/Shanghai"

imports = ["base.log_task"]

# 任务名：队列
# 可以正则匹配
task_routes_1 = {
    'celery.ping': 'default',
    'mytasks.add': 'cpu-bound',
    'feed.tasks.*': 'feeds',                           # <-- glob pattern
    re.compile(r'(image|video)\.tasks\..*'): 'media',  # <-- regex
    'video.encode': {
        'queue': 'video',
        'exchange': 'media',
        'routing_key': 'media.video.encode',
    },
}

# 可以传递方法
task_routes_2 = ('myapp.tasks.route_task', {'celery.ping': 'default'})

# 方法 myapp.tasks.route_task -> 调用 route_task
def route_task(self, name, args, kwargs, options, task=None, **kw):
    if task == 'celery.ping':
        return {'queue': 'default'}