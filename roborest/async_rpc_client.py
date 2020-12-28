import uuid
import json
from aio_pika import IncomingMessage, Message, ExchangeType


class AsyncRPCClient:

    def __init__(self,exchange_name, queue_name):
        self.loop = None
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.futures = {}

    async def connect(self, loop, channel):
        self.loop = loop
        self.channel = channel
        self.bubblehubs_exchange = await self.channel.declare_exchange(self.exchange_name, ExchangeType.DIRECT)
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.bind(self.bubblehubs_exchange)
        await self.callback_queue.consume(self.on_response)

    def on_response(self, message: IncomingMessage):
        message.ack()
        if message.correlation_id in self.futures:
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
        await self.bubblehubs_exchange.publish(
            message,
            routing_key=self.queue_name
        )

        result = await future
        return json.loads(result)

