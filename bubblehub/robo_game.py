import uuid
from robotjes.sim import Engine, Map, Success

class RoboGame:
    """ Robotjes specific game behaviour. """
    def __init__(self, mapstr):
        map = Map.fromstring(mapstr)
        self.robos = {}
        self.map = map
        self.engine = Engine(map)

    def create_robo(self):
        robo_id = str(uuid.uuid4())
        self.robos[robo_id] = {}
        # we need to place the robo in the map
        return robo_id

    def execute(self, robo_id, move):
        # execute the move for the given robo
        pass

    def fog_of_war(self, robo_id):
        # get the current 'fog-of-war' view for the given robo
        return {}

    def recording_delta (self, timeslot):
        # get the recording-delta valid since the last time this function was called
        pass
