#!/usr/bin/env python3

import sys, os, uuid
import argparse
import pika, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), os.pardir)))

PIKA_URL = 'amqp://guest:guest@localhost:5672/%2F'
QUEUE1 = 'queue1'
QUEUE2 = 'queue2'
QUEUE3 = 'queue3'

seq_nr = 0
corr_id = None
response = None


# prepare pika
parameters = pika.URLParameters(PIKA_URL)
connection = pika.adapters.blocking_connection.BlockingConnection(parameters)
channel = connection.channel()
channel.basic_qos(prefetch_count=1)
channel.queue_declare(queue=QUEUE1)
channel.queue_declare(queue=QUEUE3)
# prepare rpc receive queue (exclusive)
result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue


def rpc_request_send():
    # do the RPC call
    global corr_id, seq_nr
    corr_id = str(uuid.uuid4())
    body=f"node1_rpc[{seq_nr}]"
    seq_nr = seq_nr + 1
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE1,
        properties=pika.BasicProperties(
            reply_to=callback_queue,
            correlation_id=corr_id,
        ),
        body=body)
    connection.add_timeout(1, rpc_request_send)


def on_rpc_request_send(ch, queue,  body):
    ch.basic_publish(exchange='',
                     routing_key=queue,
                     body=body)

def on_rpc_reply_receive(ch, method, props, body):
    global corr_id
    if corr_id == props.correlation_id:
        global response
        response = body
        print(f"acked: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def on_response_receive(ch, method, props, body):
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"queue3: {body}")

channel.basic_consume(queue=callback_queue,on_message_callback=on_rpc_reply_receive)
channel.basic_consume(queue=QUEUE3, on_message_callback=on_response_receive)
timer = connection.add_timeout(1.0, rpc_request_send)

# start listening for RPC calls
try:
    channel.start_consuming()
except KeyboardInterrupt as e:
    channel.stop_consuming()
