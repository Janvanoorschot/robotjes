class DevHandler(object):

    def __init__(self, in_queue, out_queue):
        self.in_queue = in_queue
        self.out_queue = out_queue

    async def get(self):
        return self.in_queue.get()

    async def put(self, response):
        self.out_queue.put(response)
