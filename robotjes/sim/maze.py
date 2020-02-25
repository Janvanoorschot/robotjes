from .map import Map

class Maze(object):
    """A representation of a state in a Robomind Academy simulation."""

    def __init__(self, map_file):
        self.map = Map.fromfile(map_file)
        self.paints = self.map.paints_blacks()
        self.beacons = self.map.start_beacons()

        start_positions = self.map.start_positions()
        self.bot = Bot(start_positions[0], 90)

    def calc_pos(self, pos, dir, dist):
        x = pos[0]
        y = pos[1]
        if dir == 0:
            x = x + dist
        elif dir == 90:
            y = y + dist
        elif dir == 180 :
            x = x - dist
        elif dir == 270:
            y = y - dist
        new_pos = (x,y)
        if self.map.contains_pos(new_pos):
            return new_pos
        else:
            return None

    def available_pos(self, pos):
        pass



DIRS = [0, 90, 180, 270]

def dir_left(dir):
    if not dir in DIRS:
        raise ValueError(f"invalid direction {dir}")
    return (dir + 90) % 360


def dir_right(dir):
    if not dir in DIRS:
        raise ValueError(f"invalid direction {dir}")
    return (dir + 270) % 360


class Bot(object):

    def __init__(self, start_position, dir):
        self.pos = start_position
        if not dir in DIRS:
            raise ValueError(f"invalid direction {dir}")
        self.dir = dir
        self.content = []
        self.paint = None






