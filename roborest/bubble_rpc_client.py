import uuid
import json
from aio_pika import connect, IncomingMessage, Message

class BubbleRPCClient:

    def __init__(self, url, queue_name):
        self.loop = None
        self.url = url
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}

    async def connect(self, loop):
        self.loop = loop
        self.connection = await connect(self.url, loop=self.loop)
        self.channel = await self.connection.channel()
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self.on_response)

    def on_response(self, message: IncomingMessage):
        future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def call(self, cmd):
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()
        self.futures[correlation_id] = future

        body = json.dumps(cmd)
        message = Message(
            body.encode(),
            content_type="application/json",
            correlation_id=correlation_id,
            reply_to=self.callback_queue.name
        )
        await self.channel.default_exchange.publish(
            message,
            routing_key=self.queue_name
        )

        result = await future
        return json.loads(result)

