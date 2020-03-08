from .robo import Robo

# inspiration from https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call-in-python
# The goal is to execute a piece of Python code including a timeout.

TIMEOUT = 1

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
            localsParameter = {'print': print}
            try:
                with time_limit(TIMEOUT):
                    exec(data, globalsParameter, localsParameter)
            except TimeoutException as e:
                print("TimeoutException")
            except Exception as e:
                print(f"syntax error: {str(e)}")
                print(f"type script: {type(data)}")
                print(f"len script: {len(data)}")
                print(f"script: {data}")
        if "delete_me_" in script_file:
            import os
            os.unlink(script_file)

