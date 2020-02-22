class DevRequestor(object):

    def __init__(self, out_queue, in_queue):
        self.out_queue = out_queue
        self.in_queue = in_queue

    async def execute(self, cmd):
        self.out_queue.put(cmd)
        result = self.in_queue.get()
        return result
