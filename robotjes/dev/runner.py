from asyncio import Queue
from . import DevRequestor, DevHandler
from ..bot import Robo
from ..sim import Engine

class DevRunner(object):

    def __init__(self):
        self.in_queue = Queue()
        self.out_queue = Queue()
        self.requestor = DevRequestor(self.in_queue, self.out_queue)
        self.handler = DevHandler(self.out_queue, self.in_queue)
        self.robo = Robo(self.requestor)
        self.engine = Engine(self.handler)

    def run(self, map_file, script_file):
        self.engine.start(map_file)
        self.robo.start(script_file)
        recording = self.engine.get_recording()
        return recording

