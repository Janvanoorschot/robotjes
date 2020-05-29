import json
from bubblehub.model import BubbleSpec, ConnectionSpec, BubbleStatus
from monitor import wrap_monitor
from .rcp_client import RPCClient

class BubbleHub:

    def __init__(self, channel, exchange, queue):
        self.channel = channel
        self.exchange = exchange
        self.queue = queue

    # @wrap_monitor('create_bubble')
    def create_bubble(self, specs: BubbleSpec):
        body = json.dumps(specs.dict())
        self.channel.basic_publish( exchange=self.exchange,
                             routing_key=self.queue,
                             body=body)

