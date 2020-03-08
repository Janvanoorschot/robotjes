from asyncio import Queue
from . import DevRequestor, DevHandler
from robotjes.bot import RoboShell
from robotjes.sim import Engine

import asyncio
import concurrent.futures


class DevRunner(object):

    def __init__(self):
        pass

    def run(self, map_file, script_file):
        return asyncio.run(self.run_async(map_file, script_file))

    async def run_async(self, map_file, script_file):

        # prepare the objects and connect them
        queueloop = asyncio.new_event_loop()
        engine = Engine(map_file)
        cmd_queue = Queue()
        result_queue = Queue()
        requestor = DevRequestor(queueloop, cmd_queue, result_queue)
        robo_shell = RoboShell(requestor)
        handler = DevHandler(queueloop, engine, cmd_queue, result_queue)

        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ProcessPoolExecutor(2)
        f = loop.run_in_executor(executor, robo_shell.run, script_file)
        task1 = asyncio.gather(handler.run())
        task2 = asyncio.ensure_future(f)
        # loop.run_forever()

        # run client and server using asyncio
        # task1 = asyncio.gather(handler.run())
        # executer = concurrent.futures.ThreadPoolExecutor()
        # task2 = asyncio.gather(loop.run_in_executor(executer, robo_shell.run, script_file))
        # all_tasks = asyncio.gather(task1, task2)
        # loop.run_until_complete(all_tasks)
        loop.run_until_complete(task2)

        queueloop.close()


        # gather the resulting recording
        recording = engine.get_recording()
        return recording

