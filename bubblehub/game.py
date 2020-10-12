from bubblehub.model import GameSpec
from . import GameStatus, RoboGame

class Game:
    """ Represents the Game currenlty run by the Bubble.
        Current limitations:
           * only RoboGame type game is supported
           * only one robot per player
        """

    def __init__(self, owner, spec: GameSpec):
        self.owner = owner
        self.game = self.create_game(spec)
        self.game_name = spec.game_name
        self.isStarted = False
        self.isStopped = False
        self.isSuccess = False
        self.tick = 0
        self.game_tick = 0
        self.max_player_count = 1
        self.max_start_tick = 15
        self.max_tick = 30
        self.players = {}

    def create_game(self, spec: GameSpec):
        # for the time being only create RoboGame's
        mapstr = self.owner.mazes.get_map(spec.maze_id)
        return RoboGame(mapstr)

    def created(self):
        # send a status change to the games exchange
        self.owner.publish(GameStatus.CREATED, {})

    def started(self, players):
        for player_id, player in players.items():
            self.players[player_id] = {
                "player": player,
                "robo" : self.game.create_robo()
            }
        self.game_tick = 0
        self.isStarted = True
        self.isStopped = False
        self.isSuccess = True
        self.owner.publish(GameStatus.STARTED, {})

    def stopped(self):
        self.owner.publish(GameStatus.STOPPED, {})

    def is_stopped(self):
        return self.isStopped

    def result(self):
        return self.isSuccess

    def player_count(self):
        return self.max_player_count

    def get_status(self):
        return {
            "game_tick": self.game_tick,
            "isStarted": self.isStarted,
            "isStopped": self.isStopped,
            "isSuccess": self.isSuccess
        }
    def get_player_status(self, player):
        return {
            "fog_of_war": self.game.fog_of_war(player.player_id)
        }

    def status_update(self):
        self.owner.publish(GameStatus.UPDATE, {})

    def timer(self, tick):
        self.tick = tick
        if len(self.players) < self.max_player_count and self.tick > self.max_start_tick:
            self.isStopped = True
            self.isSuccess = False
        elif self.tick > self.max_tick:
            self.isStopped = True
            self.isSuccess = True
        if not self.isStopped:
            self.status_update()

    def game_timer(self, tick, moves):
        self.game_tick = self.game_tick + 1
        # feed the moves to the game
        for move in moves:
            print(f"move: {move}")
        # collect fog_of_war for each of the player/robos
        for player in self.players:
            print(f"player: {player}")
