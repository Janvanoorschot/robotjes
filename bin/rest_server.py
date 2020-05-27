#!/usr/bin/env python3

import sys, os
import argparse
import pika, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

PIKA_URL = 'amqp://guest:guest@localhost:5672/%2F'
BUBBLEHUB_QUEUE = "bubblehub_queue"
MONITOR_EXCHANGE = "monitor_exchange"
LOG_CONFIG_FILE = "bin/log.conf"

# get commandline arguments
parser = argparse.ArgumentParser(description='Start the Bubbles/Robo REST Server.')
parser.add_argument('--host', type=str, default='0.0.0.0', help='host')
parser.add_argument('--port', type=int, default=8000, help='port')
parser.add_argument('--logconf', type=str, default=LOG_CONFIG_FILE, help='port')
parser.add_argument('--pikaurl', type=str, default=PIKA_URL, help='rabbitmq url')
parser.add_argument('--bubblehubqueue', type=str, default=BUBBLEHUB_QUEUE, help='rabbitmq queue to use for rpc calls')
parser.add_argument('--monitorexchange', type=str, default=MONITOR_EXCHANGE, help='monitor exchange')
args = parser.parse_args()

# initialise the monitor module
import monitor
monitor.mon = monitor.async_monitor_client.AsyncMonitorClient(args.pikaurl, args.monitorexchange)

# initialise the roborest module
import fastapi
import roborest
from roborest.async_rpc_client import AsyncRPCClient
roborest.async_rpc_client = AsyncRPCClient(args.pikaurl, args.bubblehubqueue)
roborest.app = fastapi.FastAPI()
import roborest.bubble_hub_rest
from fastapi.staticfiles import StaticFiles
roborest.app.mount("/", StaticFiles(directory="www"), name="www")

# start the webserver (note the logging configuration)
import uvicorn
uvicorn.run(roborest.app, host=args.host, port=args.port, log_config=args.logconf)
