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
        self.max_player_count = 4
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
                "robo_id" : self.game.create_robo(player_id),
                "status": {}
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
            "recording_delta": self.game.recording_delta(),
            "isStarted": self.isStarted,
            "isStopped": self.isStopped,
            "isSuccess": self.isSuccess
        }

    def get_player_status(self, player_id):
        return {
            "fog_of_war": {
                self.players[player_id]["robo_id"]: self.players[player_id]["status"]
            }
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
        self.game.start_moves(self.game_tick)
        for player_id, move in moves.items():
            line_no = move[0]
            robo_id = move[1]
            self.game.execute(robo_id, move)
        self.game.end_moves(self.game_tick)
        # collect fog_of_war for each of the player/robos
        for player_id, player in self.players.items():
            fow = self.game.fog_of_war(player["robo_id"])
            player["status"]["fog_of_war"] = fow
            # print(f"player:{self.game_tick}/{player}")
