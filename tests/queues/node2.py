#!/usr/bin/env python3

import sys, os
import argparse
import pika, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), os.pardir)))

PIKA_URL = 'amqp://guest:guest@localhost:5672/%2F'
QUEUE1 = 'queue1'
QUEUE2 = 'queue2'
QUEUE3 = 'queue3'


def on_rpc_request_receive(ch, method, props, body):
    answer = f"answer: {body}"
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=answer)
    ch.basic_ack(delivery_tag=method.delivery_tag)


# prepare pika
parameters = pika.URLParameters(PIKA_URL)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.basic_qos(prefetch_count=1)

channel.queue_declare(queue=QUEUE1)
channel.basic_consume(queue=QUEUE1, on_message_callback=on_rpc_request_receive)

# start listening for RPC calls
try:
    channel.start_consuming()
except:
    channel.stop_consuming()
