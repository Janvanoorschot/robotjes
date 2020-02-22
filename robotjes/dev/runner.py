from asyncio import Queue
from . import DevRequestor, DevHandler
from ..bot import RoboShell
from ..sim import Engine
import asyncio

class DevRunner(object):

    def __init__(self):
        self.in_queue = Queue()
        self.out_queue = Queue()
        self.requestor = DevRequestor(self.in_queue, self.out_queue)
        self.handler = DevHandler(self.out_queue, self.in_queue)
        self.robo_shell = RoboShell(self.requestor)
        self.engine = Engine(self.handler)

    def run(self, map_file, script_file):
        # run client and server using asyncio
        loop = asyncio.get_event_loop()
        task1 = asyncio.gather(self.engine.run(map_file))
        task2 = asyncio.gather(self.robo_shell.run(script_file))
        all_tasks = asyncio.gather(task1, task2)
        results = loop.run_until_complete(all_tasks)
        loop.close()
        # gather the resulting recording
        recording = self.engine.get_recording()
        return recording

