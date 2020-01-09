import celery
from celery.exceptions import Retry
from time import sleep
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


class BaseTask(celery.Task):
    def __init__(self):
        self.name = "base_task"

    def run(self, *args, **kwargs):
        print("task run")

        # https://docs.celeryproject.org/en/latest/userguide/tasks.html#task-request
        print(self.request.id)
    
    def _task_started(self):
        pass
    
    def _task_finished(self):
        pass
    
    def task_callback(self, success):
        if success:
            print("{} finished".format(self.name))
        else:
            # 重试次数
            print(self.request.retries)
            self.retry()


class LogTask(BaseTask):
    def __init__(self):
        super(LogTask, self).__init__()
        self.name = "log_task"

    def run(self, *args, **kwargs):
        print("log task")
        print(args)
        print(kwargs)
        sleep(3)
        logger.info(kwargs)
        return "hello world"
