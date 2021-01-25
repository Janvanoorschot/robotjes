import os
import threading
import json
import socket
import datetime
import logging
logger = logging.getLogger(__name__)


class MonitorClient:

    def __init__(self, connection, exchange_name):
        self.connection = connection
        self.exchange_name = exchange_name
        self.channel = None
        self.exchange = None
        self.curtimer = None
        self.hostname = socket.gethostname()
        self.measurements = {}

    def connect(self):
        self.channel = self.connection.channel()
        self.exchange = self.channel.exchange_declare(self.exchange_name, 'fanout')
        self.curtimer = self.connection.add_timeout(1.0, self.sync_timer)

    def sync_timer(self):
        self.curtimer = self.connection.add_timeout(1.0, self.sync_timer)
        self.timer()

    def measurement(self, funname, duration):
        if funname not in self.measurements:
            self.measurements[funname] = {
                'count': 0,
                'cummulated': 0
            }
        self.measurements[funname]['count'] = self.measurements[funname]['count'] + 1
        self.measurements[funname]['cummulated'] = self.measurements[funname]['cummulated'] + duration

    def timer(self):
        if len(self.measurements) > 0:
            msg = self.build_message()
            self.send(msg)

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
        self.send(msg)

    def send(self, msg):
        try:
            if msg['process'] == 0:
                pass
            body = json.dumps(msg, default=str)
        except json.decoder.JSONDecodeError as jsonerror:
            body="{}"
        except Exception as e:
            body="{}"
        self.channel.basic_publish(exchange=self.exchange_name, routing_key='', body=body)

