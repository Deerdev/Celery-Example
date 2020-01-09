import re
from celery import app

# '任务路径'：'任务队列'
# 'feed.tasks.*' feed.tasks 下的所有任务都在 feeds queue 处理
#   - 可以是task 自定义的名称：@app.task(name="feed.tasks.search_pod")
#   - 可以是按照import的目录路径，如 base.log_task.LogTask
# 支持模糊匹配和正则
task_routes = ([
    ('feed.tasks.*', {'queue': 'feeds'}),
    ('web.tasks.*', {'queue': 'web'}),
    (re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),
],)


# 还可以是字典形式
app.conf.task_routes = {
    'mac.test1.*': {'queue': 'mac1'},
    'mac.test2.*': {'queue': 'mac2'},
    }


# 非指定的 task 会被放到默认队列 celery 处理
# 可以修改默认队列名称
app.conf.task_default_queue = 'default'


### 指定 worker 只处理指定队列
# 只处理 feeds queue
# $ celery -A proj worker -Q feeds

