from asyncio import Queue
from . import DevRequestor, DevHandler
from ..bot import RoboShell
from ..sim import Engine

import asyncio
import concurrent.futures

class DevRunner(object):

    def __init__(self):
        pass

    def run(self, map_file, script_file):
        asyncio.run(self.run_async(map_file, script_file))

    async def run_async(self, map_file, script_file):

        # prepare loop
        loop = asyncio.get_running_loop()

        # prepare the objects and connect them
        engine = Engine(map_file)
        cmd_queue = Queue()
        result_queue = Queue()
        requestor = DevRequestor(loop, cmd_queue, result_queue)
        robo_shell = RoboShell(requestor)
        handler = DevHandler(cmd_queue, result_queue, engine)

        # run client and server using asyncio
        task1 = asyncio.gather(handler.run())
        pool = concurrent.futures.ThreadPoolExecutor()
        task2 = asyncio.gather(loop.run_in_executor(pool, robo_shell.run))
        all_tasks = asyncio.gather(task1, task2)
        loop.run_until_complete(all_tasks)

        loop.close()

        # gather the resulting recording
        recording = self.engine.get_recording()
        return recording

