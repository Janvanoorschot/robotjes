#!/usr/bin/env python3

import sys, os
import argparse
import pika, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), os.pardir)))

PIKA_URL = 'amqp://guest:guest@localhost:5672/%2F'
QUEUE1 = 'queue1'
QUEUE2 = 'queue2'
QUEUE3 = 'queue3'

# prepare pika
parameters = pika.URLParameters(PIKA_URL)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.basic_qos(prefetch_count=1)


def on_response_receive(ch, method, props, body):
    ch.basic_publish(exchange='',
                     routing_key=QUEUE3,
                     body=body)


channel.queue_declare(queue=QUEUE2)
channel.queue_declare(queue=QUEUE3)
channel.basic_consume(queue=QUEUE2, on_message_callback=on_response_receive, auto_ack=True)

# start listening for RPC calls
try:
    channel.start_consuming()
except:
    channel.stop_consuming()
