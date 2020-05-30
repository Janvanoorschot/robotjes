#!/usr/bin/env python3

import sys, os, uuid
import argparse
import pika, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), os.pardir)))

PIKA_URL = 'amqp://guest:guest@localhost:5672/%2F'
QUEUE1 = 'queue1'
QUEUE2 = 'queue2'
QUEUE3 = 'queue3'

corr_id = None
response = None


def on_rpc_request_send(ch, queue,  body):
    ch.basic_publish(exchange='',
                     routing_key=queue,
                     body=body)

def on_rpc_reply_receive(ch, method, props, body):
    if corr_id == props.correlation_id:
        global response
        response = body
        print(f"node1_response: {body}")

# prepare pika
parameters = pika.URLParameters(PIKA_URL)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.basic_qos(prefetch_count=1)
channel.queue_declare(queue=QUEUE1)

# prepare rpc receive
result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue
channel.basic_consume(queue=callback_queue,on_message_callback=on_rpc_reply_receive,auto_ack=True)


# do the RPC call
corr_id = str(uuid.uuid4())
body="node1_rpc"
channel.basic_publish(
    exchange='',
    routing_key=QUEUE1,
    properties=pika.BasicProperties(
        reply_to=callback_queue,
        correlation_id=corr_id,
    ),
    body=body)




# start listening for RPC calls
try:
    while response is None:
        connection.process_data_events()
except:
    channel.stop_consuming()
