import json
import pika
import uuid
import logging
logger = logging.getLogger(__name__)
import config

from bubblehub.model import GameSpec
from . import GameStatus

class BubbleHub:

    def __init__(self):
        self.bubblehubs_exchange_name = config.BUBBLEHUBS_EXCHANGE
        self.bubbles_exchange_name = config.BUBBLES_EXCHANGE
        self.games_exchange_name = config.GAMES_EXCHANGE
        self.bubbles_queue_name = config.BUBBLES_QUEUE
        self.bubblehubs_queue_name = config.BUBBLEHUBS_QUEUE
        self.games_queue_name = None
        self.games = {}
        self.mazes = {
            "maze_id1": {"name": "maze1"},
            "maze_id2": {"name": "maze2"},
            "maze_id3": {"name": "maze3"}
        }
        self.bubbles = {}

    def connect(self, channel):
        self.channel = channel
        # create exchange/queue to and from the rest-server (we are in the consumer role)
        self.channel.exchange_declare(exchange=self.bubblehubs_exchange_name, exchange_type="direct")
        self.channel.queue_declare(queue=self.bubblehubs_queue_name)
        self.channel.queue_bind(queue=self.bubblehubs_queue_name, exchange=self.bubblehubs_exchange_name)
        self.channel.basic_consume(queue=self.bubblehubs_queue_name, on_message_callback=self.on_rest_request)
        # create exchange/queue to and from the bubbles (we are in the producers role)
        self.channel.exchange_declare(exchange=self.bubbles_exchange_name, exchange_type="direct")
        self.channel.queue_declare(queue=self.bubbles_queue_name)
        self.channel.queue_bind(queue=self.bubbles_queue_name, exchange=self.bubbles_exchange_name)
        # create exchange/queue to and from the games (run by bubbles) (we are in the consumer role)
        self.channel.exchange_declare(exchange=self.games_exchange_name, exchange_type="topic")
        result = self.channel.queue_declare('', exclusive=True)
        self.games_queue_name = result.method.queue
        self.status_routing_key = "*.status"
        channel.queue_bind(
            exchange=self.games_exchange_name,
            queue=self.games_queue_name,
            routing_key=self.status_routing_key)
        self.channel.basic_consume(
            queue=self.games_queue_name,
            on_message_callback=self.on_game_status,
            auto_ack=True
        )

    def on_rest_request(self, ch, method, props, body):
        """ do the request/run/reply cycle"""
        try:
            request = json.loads(body)
            cmd = request.get('cmd', 'unknown')
            if cmd == 'create_game':
                specs = request.get('specs', None)
                game_id = self.create_game(GameSpec.parse_obj(specs))
                reply = {'success': True, "game_id": game_id}
            elif cmd == 'list_games':
                list = self.list_games()
                reply = {'success': True, 'list': list}
            elif cmd == 'get_game':
                game_id = request.get('game_id', None)
                status = self.get_game(game_id)
                reply = {'success': True, 'status': status}
            elif cmd == 'list_mazes':
                list = self.list_mazes()
                reply = {'success': True, 'list': list}
            elif cmd == 'get_maze':
                game_id = request.get('game_id', None)
                status = self.get_game(game_id)
                reply = {'success': True, 'status': status}
            else:
                reply = {'success': False, 'error': f"unknown command: {cmd}"}
        except json.decoder.JSONDecodeError as jsonerror:
            reply = {'success': False, 'error': str(jsonerror)}
        except Exception as e:
            reply = {'success': False, 'error': str(e)}
        # send back an error-reply over 'reply_to' queue
        j = json.dumps(reply)
        ch.basic_publish(exchange=self.bubblehubs_exchange_name,
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = props.correlation_id),
                         body=j)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def on_game_status(self, ch, method, props, body):
        logger.warning(f"on_game_status {body}")
        status = json.loads(body)
        if status["bubble"] not in self.bubbles:
            self.bubbles[status["bubble"]] = status["game"]
        self.games[status["game"]] = status
        if status['state'] == GameStatus.CREATED.name:
            pass
        elif status['state'] == GameStatus.STARTED.name:
            pass
        elif status['state'] == GameStatus.IDLE.name:
            pass
        else:
            pass

    def create_game(self, specs: GameSpec):
        logger.warning("create_game")
        game_id = str(uuid.uuid4())
        request = {
            "game_id": game_id,
            "specs": specs.dict()
        }
        body = json.dumps(request)
        self.channel.basic_publish(exchange=self.bubbles_exchange_name,
                             routing_key=self.bubbles_queue_name,
                             body=body)
        return game_id

    def list_games(self):
        result = {}
        for game_id, game in self.games.items():
            if game['msg'] != GameStatus.IDLE.name:
                result[game_id] = game
        return result

    def get_game(self, game_id):
        if game_id in self.games:
            status = {
                "game_id": game_id,
                "status": self.games[game_id]
            }
        else:
            status = {
                "game_id": game_id
            }
        return status

    def list_mazes(self):
        return self.mazes

    def get_maze(self, maze_id):
        if maze_id in self.mazes:
            status = {
                "maze_id": maze_id,
                "status": self.mazes[maze_id]
            }
        else:
            status = {
                "maze_id": maze_id
            }
        return status
