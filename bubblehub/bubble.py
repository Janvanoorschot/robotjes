import json
import config
import uuid
import logging
from bubblehub.model import GameStatus, PlayerStatus
logger = logging.getLogger(__name__)

from enum import Enum
class GameState(Enum):
    IDLE = 'idle'
    CREATED = 'created'
    STARTED = 'started'
class GameInput(Enum):
    CREATING = 'creating'
    STARTING = 'starting'
    STOPPING = 'stopping'


class Bubble:

    def __init__(self, bubble_id):
        self.bubble_id = bubble_id
        self.bubbles_exchange_name = config.BUBBLES_EXCHANGE
        self.games_exchange_name = config.GAMES_EXCHANGE
        self.bubbles_queue_name = config.BUBBLES_QUEUE
        self.gamestatus_queue_name = config.GAME_STATUS_QUEUE
        self.game_duration = 10
        self.game_state = GameState.IDLE
        self.routing_key = ''

    def connect(self, channel):
        self.channel = channel
        # create exchange/queue to and from the bubbles (we are in the consumer role)
        self.channel.exchange_declare(exchange=self.bubbles_exchange_name, exchange_type="direct")
        self.channel.queue_declare(queue=self.bubbles_queue_name)
        self.channel.queue_bind(queue=self.bubbles_queue_name, exchange=self.bubbles_exchange_name)
        self.channel.basic_consume(queue=self.bubbles_queue_name, on_message_callback=self.on_hub_message)
        # create exchange/queue to and from the games (run by bubbles) (both consumer and producer role)
        self.channel.exchange_declare(exchange=self.games_exchange_name, exchange_type="topic")

    def on_hub_message(self, channel, method_frame, header_frame, body):
        logger.warning("on_hub_message")
        self.delivery_tag = method_frame.delivery_tag
        try:
            request = json.loads(body)
            game_id = request["game_id"]
            specs = request["specs"]
            self.create_game(game_id, specs)
        except json.decoder.JSONDecodeError as jsonerror:
            logger.warning(f"json error: {str(jsonerror)}")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except Exception as e:
            logger.warning(f"message error: {str(e)}")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def create_game(self, game_id, spec):
        logger.warning("start_game")
        self.game_id = game_id
        self.spec = spec
        self.timer_tick = 0
        self.game_state = GameState.CREATED
        self.routing_key = f"{self.game_id}.status"
        reply = {
            'input': GameInput.CREATING.name,
            'state': self.game_state.name,
            'bubble': self.bubble_id,
            'game': self.game_id,
            'status': self.status().dict()
        }
        j = json.dumps(reply)
        self.channel.basic_publish(
            exchange=self.games_exchange_name, routing_key=self.routing_key, body=j)

    def stop_game(self):
        logger.warning("stop_game")
        self.channel.basic_ack(delivery_tag=self.delivery_tag)
        self.game_state = GameState.IDLE
        # inform the hub
        reply = {
            'input': GameInput.STOPPING.name,
            'state': self.game_state.name,
            'bubble': self.bubble_id,
            'game': self.game_id,
            'status': self.status().dict()
        }
        j = json.dumps(reply)
        self.channel.basic_publish(
            exchange=self.games_exchange_name, routing_key=self.routing_key, body=j)

    def status(self):
        status = GameStatus(id=self.game_id, players=[])
        return status

    def timer(self, now):
        if self.game_state != GameState.IDLE:
            self.timer_tick = self.timer_tick + 1
            if self.timer_tick > self.game_duration:
                self.stop_game()
