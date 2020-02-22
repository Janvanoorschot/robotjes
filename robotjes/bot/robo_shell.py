from .robo import Robo

class RoboShell(object):

    def __init__(self, requestor):
        self.robo = Robo(requestor)

    def run(self, script_file):
        with open(script_file, 'r') as file:
            data = file.read()
        exec(data, {"robo": self.robo})

