import json
import socket
import datetime
import pika
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
        self.hostname = socket.gethostname()
        self.measurements = {}

    def connect(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
        self.channel = self.connection.channel()
        self.exchange = self.channel.exchange_declare(self.exchange_name, 'fanout')

    def measurement(self, funname, duration):
        if funname not in self.measurements:
            self.measurements[funname] = {
                'count': 0,
                'cummulated': 0
            }
        self.measurements[funname]['count'] = self.measurements[funname]['count'] + 1
        self.measurements[funname]['cummulated'] = self.measurements[funname]['cummulated'] + duration

    def timer(self):
        msg = self.build_message()
        self.send(msg)

    def build_message(self):
        msg = {}
        msg['type'] = 'responsetime'
        msg['timestamp'] = datetime.datetime.timestamp(datetime.datetime.now())
        msg['host'] = self.hostname
        msg['responsetimes'] = self.measurements
        self.measurements = {}
        return msg

    def send_log(self, msg):
        self.send(msg)

    def send(self, msg):
        try:
            body = json.dumps(msg, default=str)
        except json.decoder.JSONDecodeError as jsonerror:
            body="{}"
        except Exception as e:
            body="{}"
        self.channel.basic_publish(exchange=self.exchange_name, routing_key='', body=body)

