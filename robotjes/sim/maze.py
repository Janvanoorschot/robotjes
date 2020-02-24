from .map import Map
from .bot import Bot

class Maze(object):
    """A representation of a state in a Robomind Academy simulation."""

    def __init__(self, map_file):
        self.map = Map.fromfile(map_file)
        self.paints = self.map.start_paints()
        self.beacons = self.map.start_beacons()

        start_positions = self.map.start_positions()
        self.bot = Bot(start_positions[0])





