import asyncio
import functools
from inspect import getframeinfo, stack


class LocalRequestor(object):

    def __init__(self, loop):
        self.loop = loop
        self.command_queue = asyncio.Queue()
        self.reply_queue = asyncio.Queue()

    def execute(self, cmd):
        caller = getframeinfo(stack()[2][0])
        lineno = caller.lineno
        cmd.insert(0, lineno)
        # switch to the async environment
        future = asyncio.run_coroutine_threadsafe(functools.partial(self.async_execute,cmd), self.loop)
        return future.result()

    async def async_execute(self, cmd):
        await self.command_queue.put(cmd)
        return await self.reply_queue.get()

    async def get(self):
        pass

    async def put(self, reply):
        pass

    async def stop(self):
        pass