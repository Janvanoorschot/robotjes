from fastapi import FastAPI
app = FastAPI()

from .bubble_rpc_client import BubbleRPCClient
import asyncio
PIKA_URL = 'amqp://guest:guest@localhost:5672/%2F'
BUBBLE_QUEUE = "bubble_queue"
bubble_rpc_client = BubbleRPCClient(PIKA_URL, BUBBLE_QUEUE)

import roborest.bubble_rest


