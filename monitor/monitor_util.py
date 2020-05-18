import logging
import time
import contextlib
import inspect
logger = logging.getLogger(__name__)


class MonitorContextMonitor(contextlib.AbstractAsyncContextManager):
    def __init__(self, funname):
        self.funname = funname

    async def __aenter__(self):
        self.starttime = time.time()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        endtime = time.time()
        if endtime > self.starttime and (endtime - self.starttime) < 1000:
            duration = endtime - self.starttime
            logger.info(f"aexit {self.funname}/{duration}")


def get_monitor():
    return MonitorContextMonitor(inspect.stack()[1].function)

