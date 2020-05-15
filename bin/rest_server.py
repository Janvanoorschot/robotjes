#!/usr/bin/env python3

import sys, os
import argparse
import pika, json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

parser = argparse.ArgumentParser(description='Start the Bubbles/Robo REST Server.')
parser.add_argument('--host', type=str, default='0.0.0.0', help='host')
parser.add_argument('--port', type=int, default=8000, help='port')
args = parser.parse_args()


import uvicorn
from roborest import app
from fastapi.staticfiles import StaticFiles

app.mount("/", StaticFiles(directory="www"), name="www")
uvicorn.run(app, host=args.host, port=args.port)
