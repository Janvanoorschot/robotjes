from .robo import Robo

class RoboShell(object):

    def __init__(self, requestor):
        self.robo = Robo(requestor)

    def run(self, script_file):
        exec(script_file, {"robo": self.robo})

