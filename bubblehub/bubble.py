import json
import config
import logging
from bubblehub.model import GameState, GameSpec
from . import Game, Player
logger = logging.getLogger(__name__)

from enum import Enum

class GameStatus(Enum):
    IDLE = 'idle'
    CREATED = 'created'
    STARTED = 'started'
    STOPPED = 'stopped'

class Bubble:

    def __init__(self, bubble_id):
        self.bubble_id = bubble_id
        self.bubbles_exchange_name = config.BUBBLES_EXCHANGE
        self.games_exchange_name = config.GAMES_EXCHANGE
        self.bubbles_queue_name = config.BUBBLES_QUEUE
        self.gamestatus_queue_name = config.GAME_STATUS_QUEUE
        self.game_duration = 1000
        self.game_state = GameStatus.IDLE
        self.games_routing_key = ''
        self.game = None

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
            if self.game_state == GameStatus.IDLE:
                request = json.loads(body)
                game_id = request["game_id"]
                specs = GameSpec.parse_obj(request["specs"])
                if not self.create_game(game_id, specs):
                    logger.warning(f"creating game failed")
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except json.decoder.JSONDecodeError as jsonerror:
            logger.warning(f"json error: {str(jsonerror)}")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except Exception as e:
            logger.warning(f"message error: {str(e)}")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def on_game_message(self, channel, method_frame, header_frame, body):
        logger.warning("on_game_message")
        try:
            request = json.loads(body)
            cmd = request.get("cmd", "unknown")
            player_id = request.get("player_id", "")
            if self.game_state == GameStatus.CREATED:
                if cmd == "register":
                    player_name = request.get("player_name", "unknown")
                    password = request.get("password", "unknown")
                    if password == self.password and not self.valid_player(player_id):
                        self.register_player(player_id, player_name, password)
                    else:
                        self.disqualify_player(player_id)
                else:
                    self.disqualify_player(player_id)
            elif self.game_state == GameStatus.STARTED:
                if cmd == "":
                    pass
                else:
                    self.disqualify_player(player_id)
            elif self.game_state == GameStatus.STOPPED:
                if cmd == "":
                    pass
                else:
                    self.disqualify_player(player_id)
            else:
                self.disqualify_player(player_id)
        except json.decoder.JSONDecodeError as jsonerror:
            logger.warning(f"json error: {str(jsonerror)}")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except Exception as e:
            logger.warning(f"message error: {str(e)}")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def create_game(self, game_id: str , spec: GameSpec):
        logger.warning("start_game")
        if self.game_state == GameStatus.IDLE:
            # put ourselfs in the correct state
            self.game_id = game_id
            self.spec = spec
            self.timer_tick = 0
            self.games_routing_key = f"{self.game_id}.status"
            # create a Game instance
            self.game = Game.create(spec.maze_id)
            # start listening to messages for this game
            result = self.channel.queue_declare('', exclusive=True)
            self.game_queue_name = result.method.queue
            self.game_routing_key = f"{self.game_id}.game"
            self.channel.queue_bind(
                exchange=self.games_exchange_name,
                queue=self.game_queue_name,
                routing_key=self.game_routing_key
            )
            self.channel.basic_consume(queue=self.game_queue_name, on_message_callback=self.on_game_message, auto_ack=True)
            self.game_state = GameStatus.CREATED
            return True
        else:
            return False

        # send a status change
        reply = {
            'state': self.game_state.name,
            'bubble': self.bubble_id,
            'game': self.game_id,
            'status': self.status().dict()
        }
        j = json.dumps(reply)
        self.channel.basic_publish(
            exchange=self.games_exchange_name, routing_key=self.games_routing_key, body=j)

    def stop_game(self):
        # put ourselfs in the correct state
        logger.warning("stop_game")
        if self.game_state != GameStatus.IDLE:
            # stop listening to the queue for messages from this game
            self.channel.queue_unbind(
                exchange=self.games_exchange_name,
                queue=self.game_queue_name,
                routing_key=self.game_routing_key
            )
            # inform the hub
            reply = {
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
            self.game_state = GameStatus.IDLE
            return True
        else:
            return False

    def start_players(self):
        pass

    def valid_player(self, player_id):
        pass

    def register_player(self, player_id, player_name, password):
        pass

    def disqualify_player(self, player_id):
        pass

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
