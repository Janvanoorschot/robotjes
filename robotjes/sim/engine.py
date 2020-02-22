class Engine(object):

    def __init__(self, map_file):
        self.map_file = map_file

    def execute(self, cmd):
        cmd.append("this is a response")
        return cmd

    def get_recording(self):
        return None
