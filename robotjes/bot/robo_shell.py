from .robo import Robo

# inspiration from https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call-in-python
# The goal is to execute a piece of Python code including a timeout.

TIMEOUT = 1000

import signal
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class RoboShell(object):

    def __init__(self):
        pass

    def run(self, robo, script_file):
        with open(script_file, 'r') as file:
            data = file.read()
            globalsParameter = {'__builtins__' : None, 'robo': robo}
            localsParameter = {'print': print, 'range': range}
            try:
                with time_limit(TIMEOUT):
                    exec(data, globalsParameter, localsParameter)
            except TimeoutException as e:
                robo.message(f"script took longer then {TIMEOUT} secconds, failed by time out.")
            except Exception as e:
                robo.message(f"script failure: {str(e)}")
        if "delete_me_" in script_file:
            import os
            os.unlink(script_file)

