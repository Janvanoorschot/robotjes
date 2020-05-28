
from bubblehub.model import BubbleSpec, ConnectionSpec, BubbleStatus
from monitor import wrap_monitor
from .rcp_client import RPCClient

class BubbleHub:

    def __init__(self, channel, bubbles_queue):
        self.channel = channel
        self.bubbles_queue = bubbles_queue
        self.rpc_client = RPCClient(self.channel, self.bubbles_queue)


    @wrap_monitor('create_bubble')
    def create_bubble(self, specs: BubbleSpec, callback):
        def cb(result):
            # prepare result
            callback(result)
        # request support from (one of the) bubble
        self.rpc_client.call({'cmd': 'start_game'}, cb)

