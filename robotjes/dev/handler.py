import asyncio


class DevHandler(object):

    def __init__(self, loop, engine, cmd_queue, result_queue):
        self.loop = loop
        self.engine = engine
        self.cmd_queue = cmd_queue
        self.result_queue = result_queue

    async def run(self):
        asyncio.set_event_loop(self.loop)
        while True:
            cmd = await self.cmd_queue.get()
            result = self.engine.execute(cmd)
            if result:
                await self.result_queue.put(result)
            else:
                return

