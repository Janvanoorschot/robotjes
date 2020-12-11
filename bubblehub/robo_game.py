import uuid
from robotjes.sim import Engine, Map, Success

class RoboGame:
    """ Robotjes specific game behaviour. """
    def __init__(self, mapstr):
        self.robos = {}
        self.map = Map.fromstring(mapstr)
        self.engine = Engine(self.map)
        self.game_tick = 0
        self.last_recording_delta = 0

    def create_robo(self, player_id):
        robo_id = self.engine.create_robo()
        self.robos[robo_id] = {
            'player': player_id
        }
        return robo_id

    def destroy_robo(self, robo_id):
        self.engine.destroy_robo(robo_id)
        del self.robos[robo_id]

    def start_moves(self, game_tick):
        self.game_tick = game_tick
        self.engine.game_timer(game_tick)

    def execute(self, robo_id, move):
        # execute the move for the given robo
        self.engine.execute(robo_id, move)

    def end_moves(self, game_tick):
        pass

    def get_status(self, robo_id):
        return self.engine.get_status(robo_id)

    def recording_delta(self):
        # get the recording-delta valid since the last time this function was called
        delta = self.engine.get_recording().toMapFrom(self.last_recording_delta)
        self.last_recording_delta = self.last_recording_delta + len(delta)
        return delta

    def maze_map(self):
        return self.map.toMazeMap()

    def get_map_status(self):
        return self.engine.get_map_status()
