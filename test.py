from tasks import add

result = add.delay(1, 2)

# 返回任务是否 执行完成
# result.ready()

# 等 1 秒，返回执行结果；超过1秒就抛出异常
result.get(timeout=2)

# 不抛出异常
# result.get(propagate=False)

# 抛出异常时，打印堆栈
# result.traceback

# 任务成功与否
# result.failed()
# result.successful()

# 任务状态 PENDING -> STARTED -> SUCCESS
# result.state
