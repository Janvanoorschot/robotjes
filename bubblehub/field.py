from bubblehub.model import GameSpec
from . import GameStatus, RoboGame


class Field:
    """
        A Field where players/robots can check-in/check-out
        at will
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
        # we start the game immediatly after it is created
        self.owner.start_game()

    def started(self):
        self.game_tick = 0
        self.isStarted = True
        self.isStopped = False
        self.isSuccess = True
        self.owner.publish(GameStatus.STARTED, {})

    def stopped(self):
        self.owner.publish(GameStatus.STOPPED, {})

    def registered(self, player):
        self.players[player.player_id] = {
            "player": player,
            "robo_id": self.game.create_robo(player.player_id),
            "status": {}
        }

    def deregistered(self, player):
        self.game.destroy_robo(self.players[player.player_id]["robo_id"])
        del self.players[player.player_id]

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
        if not self.isStopped:
            self.status_update()

    def game_timer(self, tick, moves):
        self.game_tick = self.game_tick + 1
        self.game.start_moves(self.game_tick)
        for player_id, move in moves.items():
            line_no = move[0]
            robo_id = move[1]
            self.game.execute(robo_id, move)
        self.game.end_moves(self.game_tick)
        for player_id, player in self.players.items():
            fow = self.game.fog_of_war(player["robo_id"])
            player["status"]["fog_of_war"] = fow
