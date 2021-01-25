import time
import contextlib
import inspect
from robotjessrv.server import monitor
from functools import wraps


class MonitorContextMonitor(contextlib.AbstractAsyncContextManager):
    def __init__(self, funname):
        self.funname = funname

    async def __aenter__(self):
        self.starttime = time.time()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        endtime = time.time()
        if endtime > self.starttime and (endtime - self.starttime) < 1000:
            duration = endtime - self.starttime
            monitor.mon.measurement(self.funname, duration)


def get_monitor():
    """ Monitoring feature to be used inside a function using 'with'."""
    return MonitorContextMonitor(inspect.stack()[1].function)


def wrap_monitor(funname):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            starttime = time.time()
            result = f(*args, **kwargs)
            endtime = time.time()
            duration = endtime - starttime
            monitor.mon.measurement(funname, duration)
            return result
        return wrapper
    return decorator

