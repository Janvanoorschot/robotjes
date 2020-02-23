class Handler(object):

    def __init__(self, cmd_queue, result_queue, engine):
        self.cmd_queue = cmd_queue
        self.result_queue = result_queue
        self.engine = engine

    async def run(self):
        cmd = await self.cmd_queue.get()
        result = self.engine.execute(cmd)
        await self.result_queue.put(result)

