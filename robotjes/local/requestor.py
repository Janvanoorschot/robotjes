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
        future = asyncio.run_coroutine_threadsafe(self.async_execute(cmd), self.loop)
        return future.result()

    async def async_execute(self, cmd):
        await self.command_queue.put(cmd)
        reply = await self.reply_queue.get()
        return reply

    async def get(self):
        return await self.command_queue.get()

    async def put(self, reply):
        await self.reply_queue.put(reply)

    async def stop(self):
        pass