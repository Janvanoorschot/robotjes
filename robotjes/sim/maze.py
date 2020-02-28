from .map import Map

class Maze(object):

    # directions
    LEFT = 90
    FRONT = 0
    RIGHT = 270
    BACK = 180

    # status of position
    CLEAR = 1
    BEACON = 2
    WHITE = 3
    BLACK = 4
    NOPAINT = 5

    def __init__(self, map_file):
        self.map = Map.fromfile(map_file)
        self.paints_black = set(self.map.paints_blacks())
        self.paints_white = set(self.map.paints_whites())
        self.beacons = set(self.map.start_beacons())

        start_positions = self.map.start_positions()
        self.bot = Bot(start_positions[0], 90)

    def available_pos(self, pos):
        return self.map.available_pos() and not pos in self.beacons and not pos != self.bot.pos

    def move_to(self, pos):
        if self.map.available_pos() and not pos in self.beacons:
            self.bot.pos = pos

    def left(self):
        return self.bot.left()

    def right(self):
        return self.bot.right()

    def pickUp(self):
        if self.check(Maze.FRONT, Maze.BEACON):
            front = calc_pos(self.bot.pos, self.FRONT, 1)
            self.beacons.remove(front)
            self.bot.beacons.add(front)
            return True
        else:
            return False

    def eatUp(self):
        if self.check(Maze.FRONT, Maze.BEACON):
            front = calc_pos(self.bot.pos, self.FRONT, 1)
            self.beacons.remove(front)
            return True
        else:
            return False

    def putDown(self):
        if self.check(Maze.FRONT, Maze.CLEAR) and len(self.bot.beacons) > 0:
            front = calc_pos(self.bot.pos, self.FRONT, 1)
            self.bot.beacons.remove(front)
            self.beacons.add(front)
            return True
        else:
            return False

    def paintWhite(self):
        self.paints_black.remove(self.bot.pos)
        self.paints_white.add(self.bot.pos)
        self.bot.paint = self.WHITE
        return True

    def paintBlack(self):
        self.paints_white.remove(self.bot.pos)
        self.paints_black.add(self.bot.pos)
        self.bot.paint = self.BLACK
        return True

    def stopPainting(self):
        self.bot.paint = self.NOPAINT
        return True

    def check(self, dir, cond):
        pass

    def flipCoin(self):
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


class Bot(object):

    def __init__(self, start_position, dir):
        self.pos = start_position
        if not dir in DIRS:
            raise ValueError(f"invalid direction {dir}")
        self.dir = dir
        self.beacons = set()
        self.paint = None

    def left(self):
        self.pos = dir_left(self.pos)
        return self.pos

    def right(self):
        self.pos = dir_right(self.pos)
        return self.pos






