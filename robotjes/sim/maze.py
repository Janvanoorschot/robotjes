from .map import Map

class Maze(object):
    """A representation of a state in a Robomind Academy simulation."""

    def __init__(self, map_file):
        self.map = Map.fromfile(map_file)
        self.bots = self.map.start_bots()
        self.paints = self.map.start_paints()
        self.beacons = self.map.start_beacons()





