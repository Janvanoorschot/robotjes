from .robo import Robo

# inspiration from https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call-in-python
# The goal is to execute a piece of Python code including a timeout.

TIMEOUT = 1

from multiprocessing import Process
from time import sleep

def f(time):
    sleep(time)


def run_with_limited_time(func, args, kwargs, time):
    """Runs a function with time limit

    :param func: The function to run
    :param args: The functions args, given as tuple
    :param kwargs: The functions keywords, given as dict
    :param time: The time limit in seconds
    :return: True if the function ended successfully. False if it was terminated.
    """
    p = Process(target=func, args=args, kwargs=kwargs)
    p.start()
    p.join(time)
    if p.is_alive():
        p.terminate()
        return False

    return True

class RoboShell(object):

    def __init__(self):
        pass

    def run(self, robo, script_file):
        with open(script_file, 'r') as file:
            data = file.read()
            globalsParameter = {'__builtins__' : None, 'robo': robo}
            localsParameter = {'print': print, 'range': range, 'quit': quit}
            if run_with_limited_time(exec, (data, globalsParameter, localsParameter), {}, TIMEOUT):
                pass
            else:
                robo.message(f"script took longer then {TIMEOUT} secconds, failed by time out.")
        if "delete_me_" in script_file:
            import os
            os.unlink(script_file)

