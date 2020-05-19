#!/usr/bin/env python3

import sys, os
import argparse
import pika, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

# get commandline arguments
parser = argparse.ArgumentParser(description='Start the Bubbles/Robo REST Server.')
parser.add_argument('--host', type=str, default='0.0.0.0', help='host')
parser.add_argument('--port', type=int, default=8000, help='port')
args = parser.parse_args()

PIKA_URL = 'amqp://guest:guest@localhost:5672/%2F'
BUBBLE_QUEUE = "bubble_queue"
MONITOR_EXCHANGE = "monitor_exchange"

# initialise the monitor module
import asyncio
import monitor
monitor.mon = monitor.monitor_client.MonitorClient(PIKA_URL, MONITOR_EXCHANGE)

# initialise the roborest module
import fastapi
import roborest
from roborest.bubble_rpc_client import BubbleRPCClient
roborest.bubble_rpc_client = BubbleRPCClient(PIKA_URL, BUBBLE_QUEUE)
roborest.app = fastapi.FastAPI()
import roborest.bubble_rest
from fastapi.staticfiles import StaticFiles
roborest.app.mount("/", StaticFiles(directory="www"), name="www")

# start the webserver (note the logging configuration)
import uvicorn
uvicorn.run(roborest.app, host=args.host, port=args.port, log_config="bin/log.conf")
