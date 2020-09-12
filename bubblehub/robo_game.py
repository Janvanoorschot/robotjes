from robotjes.sim import Engine, Map, Success

class RoboGame:
    """ Robotjes specific game behaviour. """
    def __init__(self, mapstr):
        map = Map.fromstring(mapstr)
        self.map = map
        self.engine = Engine(map)

    def execute(self, robo_id, move):
        # execute the move for the given robo
        pass

    def fog_of_war(self, robo_id):
        # get the current 'fog-of-war' view for the given robo
        pass

    def recording_delta (self, timeslot):
        # get the recording-delta valid since the last time this function was called
        pass
