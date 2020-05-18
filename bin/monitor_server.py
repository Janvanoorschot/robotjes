#!/usr/bin/env python3

import pika
import json
import sys, os
import argparse
from monitor import MonitorServer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
PIKA_URL = 'amqp://guest:guest@localhost:5672/%2F'
MONITOR_EXCHANGE = "monitor_exchange"

# get commandline arguments
parser = argparse.ArgumentParser(description='Start the Monitor Server.')
# parser.add_argument('--host', type=str, default='0.0.0.0', help='host')
args = parser.parse_args()

# create our monitor-server object
monitor_server = MonitorServer()

def on_request(ch, method, props, body):
    """ do the request/run/reply cycle"""
    try:
        request = json.loads(body)
        monitor_server.handle(request)
    except json.decoder.JSONDecodeError as jsonerror:
        pass
    except Exception as e:
        pass

# prepare pika (blocking, one RPC queue and a requestor-created reply-to queue)
parameters = pika.URLParameters(PIKA_URL)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange=MONITOR_EXCHANGE, exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange=MONITOR_EXCHANGE, queue=queue_name)

# start listening for work
channel.basic_consume(queue=queue_name, on_message_callback=on_request, auto_ack=True)
channel.start_consuming()
