import json
from aio_pika import connect, ExchangeType, Message
import logging
logger = logging.getLogger(__name__)


class MonitorClient:

    def __init__(self, url, exchange_name):
        self.url = url
        self.exchange_name = exchange_name
        self.loop = None
        self.connection = None
        self.channel = None
        self.exchange = None
        self.measurements = {}

    async def connect(self, loop):
        self.loop = loop
        self.connection = await connect(self.url, loop=self.loop)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(self.exchange_name, ExchangeType.FANOUT)

    def measurement(self, funname, duration):
        if funname not in self.measurements:
            self.measurements[funname] = {
                'count': 0,
                'cummulated': 0
            }
        self.measurements[funname]['count'] = self.measurements[funname]['count'] + 1
        self.measurements[funname]['cummulated'] = self.measurements[funname]['cummulated'] + duration

    async def timer(self):
        await self.send(self.measurements)
        self.measurements = {}

    async def send(self, msg):
        body = json.dumps(msg)
        message = Message(
            body.encode(),
            content_type="application/json"
        )
        await self.exchange.publish(
            message,
            routing_key=''
        )

