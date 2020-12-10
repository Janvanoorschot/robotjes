import json
import config
import logging
from bubblehub.model import GameState, GameSpec
from . import Field, Game, Player, GameStatus
logger = logging.getLogger(__name__)


class Bubble:

    def __init__(self, bubble_id):
        self.bubble_id = bubble_id
        self.bubbles_exchange_name = config.BUBBLES_EXCHANGE
        self.games_exchange_name = config.GAMES_EXCHANGE
        self.bubbles_queue_name = config.BUBBLES_QUEUE
        self.gamestatus_queue_name = config.GAME_STATUS_QUEUE
        self.game_password = None
        self.game_state = GameStatus.IDLE
        self.game_out_routing_key = ''
        self.game = None
        self.players = {}
        self.moves = {}
        self.channel = None
        self.delivery_tag = None
        self.now = None
        self.starttime = None
        self.mazes = None
        self.tick = 0
        self.resolution = 5

    def set_mazes(self, mazes):
        self.mazes = mazes

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
        self.delivery_tag = method_frame.delivery_tag
        if self.game_state != GameStatus.IDLE:
            # busy, try someplace else
            channel.basic_reject(self.delivery_tag, requeue=True)
            return
        try:
            # for the time being, the only message from bubble-hub is 'create-game'
            if self.game_state == GameStatus.IDLE:
                request = json.loads(body)
                game_id = request["game_id"]
                specs = GameSpec.parse_obj(request["specs"])
                if not self.create_game(game_id, specs):
                    logger.warning(f"creating game failed")
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                else:
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except json.decoder.JSONDecodeError as jsonerror:
            logger.warning(f"json error: {str(jsonerror)}")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        except Exception as e:
            logger.warning(f"message error: {str(e)}")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def create_game(self, game_id: str , spec: GameSpec):
        logger.warning("create_game")
        if self.game_state == GameStatus.IDLE:
            # put ourselfs in the correct state
            self.tick = 0
            self.game_id = game_id
            self.game_password = spec.game_password
            self.spec = spec
            self.game_out_routing_key = f"{self.game_id}.status"
            # create a Game instance
            self.game = Field(self, spec)
            # initialise the player store for this game in this Bubble
            self.start_players()
            # start listening to messages for this game
            result = self.channel.queue_declare('', exclusive=True)
            self.game_queue_name = result.method.queue
            self.game_in_routing_key = f"{self.game_id}.game"
            self.channel.queue_bind(
                exchange=self.games_exchange_name,
                queue=self.game_queue_name,
                routing_key=self.game_in_routing_key
            )
            self.channel.basic_consume(queue=self.game_queue_name, on_message_callback=self.on_game_message, auto_ack=True)
            self.game_state = GameStatus.CREATED
            self.starttime = self.now
            self.game.created()
            return True
        else:
            return False

    def start_game(self):
        logger.warning("start_game")
        self.game.started()
        self.game_state = GameStatus.STARTED

    def stop_game(self):
        if self.game_state == GameStatus.CREATED or self.game_state == GameStatus.STARTED:
            logger.warning("stop_game")
            # stop listening to the queue for messages from this game
            self.channel.queue_unbind(
                exchange=self.games_exchange_name,
                queue=self.game_queue_name,
                routing_key=self.game_in_routing_key
            )
            # send game result to anyone interested (probably the hub)
            self.game_state = GameStatus.IDLE
            self.game.stopped()
            return True
        else:
            return False

    def start_players(self):
        self.players = {}
        self.invalid_players = {}

    def is_valid_player(self, player_id):
        return player_id in self.players and not player_id in self.invalid_players

    def register_player(self, player_id, player_name):
        if player_id in self.players or player_id in self.invalid_players:
            self.disqualify_player(player_id)
        if len(self.players) < self.game.player_count():
            # we can handle a new player
            player = Player(player_id, player_name)
            self.players[player_id] = player
            self.game.registered(player)

    def deregister_player(self, player_id):
        if player_id in self.players:
            player = self.players[player_id]
            del self.players[player_id]
            self.game.deregistered(player)

    def disqualify_player(self, player_id):
        if player_id in self.players:
            self.invalid_players[player_id] = self.players[player_id]
        else:
            self.invalid_players[player_id] = None

    def on_game_message(self, channel, method_frame, header_frame, body):
        try:
            request = json.loads(body)
            cmd = request.get("cmd", "unknown")
            player_id = request.get("player_id", "")
            if self.game_state == GameStatus.CREATED:
                pass
            elif self.game_state == GameStatus.STARTED:
                if cmd == "register":
                    player_name = request.get("player_name", "unknown")
                    password = request.get("password", "unknown")
                    if password == self.game_password and not self.is_valid_player(player_id):
                        self.register_player(player_id, player_name)
                    else:
                        self.disqualify_player(player_id)
                elif cmd == "deregister":
                    player_id = request.get("player_id", "unknown")
                    if player_id in self.players:
                        self.deregister_player(player_id)
                elif cmd == "move":
                    player_id = request.get("player_id", "unknown")
                    move = request.get("move", {})
                    if player_id in self.players:
                        self.moves[player_id] = move
                else:
                    self.disqualify_player(player_id)
            elif self.game_state == GameStatus.STOPPED:
                pass
            else:
                self.disqualify_player(player_id)
        except json.decoder.JSONDecodeError as jsonerror:
            logger.warning(f"json error: {str(jsonerror)}")
        except Exception as e:
            logger.warning(f"message error: {str(e)}")

    def publish(self, msg: GameStatus, data: dict):
        if not self.game:
            item = {
                'bubble_id': self.bubble_id,
                'game_id': "unknown",
                'game_name': "unknown",
                'status': {},
                'players': [],
                'msg': msg.name,
                'tick': self.tick,
                'data': data
            }
        else:
            print(f"bubble/publish/{self.now}")
            players_status = []
            for player_id, player in self.players.items():
                players_status.append({
                    "player_id": player_id,
                    "player_name": player.player_name,
                    "player_status": self.game.get_player_status(player_id)
                })
            item = {
                'bubble_id': self.bubble_id,
                'game_id': self.game_id,
                'game_name': self.game.game_name,
                'status': self.game.get_game_status(),
                'mapstatus': self.game.get_map_status(),
                'players': players_status,
                'msg': msg.name,
                'tick': self.tick,
                'data': data
            }
        try:
            j = json.dumps(item)
        except TypeError as te:
            print(f"error: {te}")
        self.channel.basic_publish(
            exchange=self.games_exchange_name,
            routing_key=self.game_out_routing_key,
            body=j)

    def timer(self, now):
        self.now = now
        if self.now and self.starttime:
            self.tick = self.tick + 1
        else:
            self.tick = 0
        if self.game_state == GameStatus.CREATED or self.game_state == GameStatus.STARTED:
            self.game.timer(self.tick)
            if self.game_state == GameStatus.STARTED:
                if self.tick % self.resolution == 0:
                    print(f"bubble/timer/{self.now}")
                    self.game.game_timer(self.tick/self.resolution, self.moves)
                    self.moves.clear()
            if self.game.is_stopped():
                self.stop_game()
