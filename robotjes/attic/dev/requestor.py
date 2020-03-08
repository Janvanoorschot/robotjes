import asyncio


class DevRequestor(object):

    def __init__(self, loop, cmd_queue, result_queue):
        self.loop = loop
        self.cmd_queue = cmd_queue
        self.result_queue = result_queue

    def execute(self, cmd):
        future = asyncio.run_coroutine_threadsafe(self.async_execute(cmd), self.loop)
        return future.result()

    async def async_execute(self, cmd):
        await self.cmd_queue.put(cmd)
        result = await self.result_queue.get()
        return result

