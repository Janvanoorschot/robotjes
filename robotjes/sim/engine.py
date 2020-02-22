class Engine(object):

    def __init__(self, handler):
        self.handler = handler

    def run(self, map_file):
        ready = False
        while not ready:
            cmd = self.handler.get()
            cmd.append("this is a response")
            self.handler.put(cmd)
            ready = True

