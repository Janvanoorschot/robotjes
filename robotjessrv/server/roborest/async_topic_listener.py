from aio_pika import IncomingMessage, ExchangeType
import json

class AsyncTopicListener:

    def __init__(self,exchange_name, routing_key, listener):
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.listener = listener
        self.exchange = None
        self.connection = None
        self.loop = None
        self.channel = None

    async def connect(self, loop, channel):
        self.loop = loop
        self.channel = channel
        self.exchange = await self.channel.declare_exchange(self.exchange_name, ExchangeType.TOPIC)
        self.listen_queue = await self.channel.declare_queue(exclusive=True)
        await self.listen_queue.bind(self.exchange, self.routing_key)
        await self.listen_queue.consume(self.on_message)

    def on_message(self, message: IncomingMessage):
        message.ack()
        routing_key = message.routing_key
        body = message.body.decode()
        self.listener(routing_key, json.loads(body))

