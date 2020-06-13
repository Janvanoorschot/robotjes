import json
from bubblehub.model import BubbleSpec

class BubbleHub:

    def __init__(self, channel, exchange, queue):
        self.channel = channel
        self.exchange = exchange
        self.queue = queue

    def create_bubble(self, specs: BubbleSpec):
        body = json.dumps(specs.dict())
        self.channel.basic_publish(exchange=self.exchange,
                             routing_key=self.queue,
                             body=body)

