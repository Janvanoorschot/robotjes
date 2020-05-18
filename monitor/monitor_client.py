import json
from aio_pika import connect, ExchangeType, Message


class MonitorClient:

    def __init(self, url, exchange_name):
        self.url = url
        self.exchange_name = exchange_name
        self.loop = None
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self, loop):
        self.loop = loop
        self.connection = await connect(self.url, loop=self.loop)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(self.exchange_name, ExchangeType.FANOUT)

    async def send(self, msg):
        body = json.dumps(msg)
        message = Message(
            body.encode(),
            content_type="application/json"
        )
        await self.exchange.publish(
            message,
            routing_key="monitor"
        )

