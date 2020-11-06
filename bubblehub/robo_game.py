import uuid
from robotjes.sim import Engine, Map, Success

class RoboGame:
    """ Robotjes specific game behaviour. """
    def __init__(self, mapstr):
        map = Map.fromstring(mapstr)
        self.robos = {}
        self.map = map
        self.engine = Engine(map)
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

    def fog_of_war(self, robo_id):
        # get the current 'fog-of-war' view for the given robo
        return {
            "robo": robo_id,
            "game_tick": self.game_tick,
            "fog_of_war": self.engine.fog_of_war(robo_id)
        }

    def recording_delta (self):
        # get the recording-delta valid since the last time this function was called
        delta = self.engine.get_recording().toMapFrom(self.last_recording_delta)
        self.last_recording_delta = self.last_recording_delta + len(delta)
        return delta
