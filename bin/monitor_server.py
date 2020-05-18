#!/usr/bin/env python3

import pika
import json
import sys, os
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

# get commandline arguments
parser = argparse.ArgumentParser(description='Start the Monitor Server.')
# parser.add_argument('--host', type=str, default='0.0.0.0', help='host')
args = parser.parse_args()

PIKA_URL = 'amqp://guest:guest@localhost:5672/%2F'
MONITOR_EXCHANGE = "monitor_exchange"

def on_request(ch, method, props, body):
    """ do the request/run/reply cycle"""
    try:
        request = json.loads(body)
        # do some work
        if "map" in request and "success" in request and "script" in request:
            map = request["map"]
            success = request["success"]
            script = request["script"]
            reply = {}
        else:
            reply = {'error': "missing components in request"}
    except json.decoder.JSONDecodeError as jsonerror:
        reply = {'error': str(jsonerror)}
    except Exception as e:
        reply = {'error': str(e)}

    # send back reply over 'reply_to' queue
    j = json.dumps(reply)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=j)
    ch.basic_ack(delivery_tag=method.delivery_tag)

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
