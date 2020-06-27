import json
import config
import uuid
import logging
from bubblehub.model import GameState, PlayerState
logger = logging.getLogger(__name__)

from enum import Enum
class GameStatus(Enum):
    IDLE = 'idle'
    CREATED = 'created'
    STARTED = 'started'
    STOPPED = 'stopped'

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
        self.game_state = GameStatus.IDLE
        self.games_routing_key = ''

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
            # for the time being, the only message from bubble-hub is 'create-game'
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
        # put ourselfs in the correct state
        self.game_id = game_id
        self.spec = spec
        self.timer_tick = 0
        self.game_state = GameStatus.CREATED
        self.games_routing_key = f"{self.game_id}.status"
        # start listening to messages for this game
        result = self.channel.queue_declare('', exclusive=True)
        self.game_queue_name = result.method.queue
        self.game_routing_key = f"{self.game_id}.game"
        self.channel.queue_bind(
            exchange=self.games_exchange_name,
            queue=self.game_queue_name,
            routing_key=self.game_routing_key
        )
        self.channel.basic_consume(queue=self.game_queue_name, on_message_callback=self.on_game_message)

        # send a status change
        reply = {
            'input': GameInput.CREATING.name,
            'state': self.game_state.name,
            'bubble': self.bubble_id,
            'game': self.game_id,
            'status': self.status().dict()
        }
        j = json.dumps(reply)
        self.channel.basic_publish(
            exchange=self.games_exchange_name, routing_key=self.games_routing_key, body=j)

    def on_game_message(self, channel, method_frame, header_frame, body):
        logger.warning("on_game_message")
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

    def stop_game(self):
        # put ourselfs in the correct state
        logger.warning("stop_game")
        self.game_state = GameStatus.IDLE
        # stop listening to the queue for messages from this game
        self.channel.queue_unbind(
            exchange=self.games_exchange_name,
            queue=self.game_queue_name,
            routing_key=self.game_routing_key
        )
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
            exchange=self.games_exchange_name, routing_key=self.games_routing_key, body=j)
        # we only now can ACK the 'create-game' message
        self.channel.basic_ack(delivery_tag=self.delivery_tag)


    def status(self):
        status = GameState(
            id=self.game_id,
            status=self.game_state.name,
            players=[])
        return status

    def timer(self, now):
        if self.game_state != GameStatus.IDLE:
            self.timer_tick = self.timer_tick + 1
            if self.timer_tick > self.game_duration:
                self.stop_game()
