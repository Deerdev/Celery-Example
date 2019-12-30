from __future__ import absolute_import, unicode_literals
from .celery import app
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

# bind 将函数第一个参数绑定为 task instance
@app.task(bind=True)
def add2(self, x, y):
    logger.info(self.request.id)


# retry
@app.task(bind=True, default_retry_delay=30 * 60)  # retry in 30 minutes.
def add(self, x, y):
    try:
        pass
        # something_raising()
    except Exception as exc:
        # overrides the default delay to retry after 1 minute
        raise self.retry(exc=exc, countdown=60)
        # retry 会继续抛出异常，celery.exceptions.Retry 异常

# 针对特定的错误 retry，设置retry次数
@app.task(autoretry_for=(FailWhaleError,),
          retry_kwargs={'max_retries': 5})
def refresh_timeline(user):
    return twitter.refresh_timeline(user)

@app.task(bind=True)
def refresh_timeline(self, user):
    try:
        twitter.refresh_timeline(user)
    except FailWhaleError as exc:
        raise self.retry(exc=exc, max_retries=5)


# start
# $ celery -A proj worker -l info

# 启动信息
# [config]
# .> app:         proj:0x10e5a4cf8
# .> transport:   redis://127.0.0.1:6379/0
# .> results:     redis://127.0.0.1/1
# .> concurrency: 12 (prefork)
# .> task events: OFF (enable -E to monitor tasks in this worker)
#
# [queues]
# .> celery           exchange=celery(direct) key=celery

# – Concurrency is the number of prefork worker process(多进程模式) used to process your tasks concurrently
#   默认为CPU核数 x2
# - task events: 发送监控信息
# – Queues is the list of queues that the worker will consume tasks from.
#   The worker can be told to consume from several queues at once
#   使用 Route 配置队列



# run celery in background
# celery multi start w1 -A proj -l info
# celery  multi restart w1 -A proj -l info
# celery multi stop w1 -A proj -l info
# 等待worker运行完，再 stop
# celery multi stopwait w1 -A proj -l info

# 配置 pidfile 和 logfile，不同的 worker 写到不同的文件中
# celery multi start w1 -A proj -l info --pidfile=/var/run/celery/%n.pid \
#                                         --logfile=/var/log/celery/%n%I.log

# signature 签名
add.signature((2, 2), countdown=10)
s1 = add.s(2, 2) # 简写
# 等同于 tasks.add(2, 2)

res = s1.delay()
res.get() # 4





from celery import group, chain, chord

# Group 任务
# 并行执行任务
group(add.s(i, i) for i in xrange(10))().get()
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# g(10) 在循环的基础上 +10
g = group(add.s(i) for i in xrange(10))
g(10).get()
# [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

# Chains
# 链式调用，上一个任务的返回传递给下一个任务
chain(add.s(4, 4) | mul.s(8))().get()  # 简写： (add.s(4, 4) | mul.s(8))().get()
# (4 + 4) * 8

# (? + 4) * 8
g = chain(add.s(4) | mul.s(8))
g(4).get()
# 64


# Chords
# 给 group 任务加一个callback
chord((add.s(i, i) for i in xrange(10)), xsum.s())().get()
# sum([0, 2, 4, 6, 8, 10, 12, 14, 16, 18]) = 90
# 下同
(group(add.s(i, i) for i in xrange(10)) | xsum.s())().get()

# See More：[Canvas: Designing Work-flows](http://docs.celeryproject.org/en/latest/userguide/canvas.html#guide-canvas)


