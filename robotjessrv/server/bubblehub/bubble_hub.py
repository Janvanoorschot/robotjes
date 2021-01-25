import json
import pika
import uuid
import logging
logger = logging.getLogger(__name__)
from robotjessrv import config
from robotjessrv.server.bubblehub.model import GameSpec


class BubbleHub:

    def __init__(self):
        self.bubblehubs_exchange_name = config.BUBBLEHUBS_EXCHANGE
        self.bubbles_exchange_name = config.BUBBLES_EXCHANGE
        self.games_exchange_name = config.GAMES_EXCHANGE
        self.bubbles_queue_name = config.BUBBLES_QUEUE
        self.bubblehubs_queue_name = config.BUBBLEHUBS_QUEUE
        self.games_queue_name = None
        self.mazes = None

    def set_mazes(self, mazes):
        self.mazes = mazes

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

    def on_rest_request(self, ch, method, props, body):
        """ do the request/run/reply cycle"""
        try:
            request = json.loads(body)
            cmd = request.get('cmd', 'unknown')
            if cmd == 'create_game':
                specs = request.get('specs', None)
                game_id = self.create_game(GameSpec.parse_obj(specs))
                reply = {'success': True, "game_id": game_id}
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

    def list_mazes(self):
        return self.mazes.list_mazes()

    def get_maze(self, maze_id):
        return self.mazes.status_maze(maze_id)
