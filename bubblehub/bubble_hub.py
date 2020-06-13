import json
from bubblehub.model import BubbleSpec
import config

class BubbleHub:

    def __init__(self, channel):
        self.channel = channel

    def create_bubble(self, specs: BubbleSpec):
        body = json.dumps(specs.dict())
        self.channel.basic_publish(exchange=config.BUBBLES_EXCHANGE,
                             routing_key=config.BUBBLES_QUEUE,
                             body=body)

