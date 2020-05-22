import os
import threading
import asyncio
import json
import socket
import datetime
from aio_pika import connect, ExchangeType, Message
import logging
logger = logging.getLogger(__name__)


class AsyncMonitorClient:

    def __init__(self, url, exchange_name):
        self.url = url
        self.exchange_name = exchange_name
        self.loop = None
        self.connection = None
        self.channel = None
        self.exchange = None
        self.hostname = socket.gethostname()
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
        msg = self.build_message()
        await self.send(msg)

    def build_message(self):
        msg = {}
        msg['type'] = 'responsetime'
        msg['timestamp'] = datetime.datetime.timestamp(datetime.datetime.now())
        msg['host'] = self.hostname
        msg['process'] = os.getpid()
        msg['thread'] = threading.get_ident()
        msg['responsetimes'] = self.measurements
        self.measurements = {}
        return msg

    def send_log(self, msg):
        if self.loop:
            asyncio.create_task(self.do_send_log(msg))

    async def do_send_log(self, msg):
        try:
            await self.send(msg)
        except Exception as e:
            print(f"error!!!!!!!!!!!! {str(e)}")

    async def send(self, msg):
        try:
            body = json.dumps(msg, default=str)
        except json.decoder.JSONDecodeError as jsonerror:
            body="{}"
        except Exception as e:
            body="{}"
        message = Message(
            body.encode(),
            content_type="application/json"
        )
        await self.exchange.publish(
            message,
            routing_key=''
        )

