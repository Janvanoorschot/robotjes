import json
import config
import uuid
import logging
logger = logging.getLogger(__name__)

class Bubble:

    def __init__(self, bubble_id):
        self.bubble_id = bubble_id
        self.bubbles_exchange_name = config.BUBBLES_EXCHANGE
        self.games_exchange_name = config.GAMES_EXCHANGE
        self.bubbles_queue_name = config.BUBBLES_QUEUE
        self.gamestatus_queue_name = config.GAME_STATUS_QUEUE

    def connect(self, channel):
        self.channel = channel
        # create exchange/queue to and from the bubbles (we are in the consumer role)
        self.channel.exchange_declare(exchange=self.bubbles_exchange_name, exchange_type="direct")
        self.channel.queue_declare(queue=self.bubbles_queue_name)
        self.channel.queue_bind(queue=self.bubbles_queue_name, exchange=self.bubbles_exchange_name)
        self.channel.basic_consume(queue=self.bubbles_queue_name, on_message_callback=self.on_hub_message)
        # create exchange/queue to and from the games (run by bubbles) (both consumer and producer role)
        self.channel.exchange_declare(exchange=self.games_exchange_name, exchange_type="direct")
        self.channel.queue_declare(queue=self.bubbles_queue_name)
        self.channel.queue_bind(queue=self.bubbles_queue_name, exchange=self.games_exchange_name)

    def on_hub_message(self, channel, method_frame, header_frame, body):
        self.delivery_tag = method_frame.delivery_tag
        try:
            specs = json.loads(body)
            game_id = str(uuid.uuid4())
            self.start_game(game_id, specs)
        except json.decoder.JSONDecodeError as jsonerror:
            logger.warning(f"json error: {str(jsonerror)}")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except Exception as e:
            logger.warning(f"message error: {str(e)}")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def start_game(self, game_id, spec):
        self.game_id = game_id
        self.spec = spec
        # print(f"before queue_bind: {self.queue_in_name}/{self.game_id}")
        # self.channel.queue_bind(
        #     exchange=config.GAME_IN_EXCHANGE,
        #     queue=self.queue_in_name,
        #     routing_key=self.game_id
        # )
        # reply = {
        #     'cmd': "starting",
        #     'bubble': self.bubble_id,
        #     'game': self.game_id
        # }
        # j = json.dumps(reply)
        # self.channel.basic_publish(exchange=self.games_exchange_name,
        #                            routing_key=self.gamestatus_queue_name,
        #                            body=j)

    def timer(self, now):
        pass
