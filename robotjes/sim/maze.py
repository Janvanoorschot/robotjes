import random
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
        return self.map.available_pos(pos) and not pos in self.beacons and pos != self.bot.pos

    def calc_pos(self, pos, dir, dist):
        x = pos[0]
        y = pos[1]
        if dir == 0:
            x = x + dist
        elif dir == 90:
            y = y - dist
        elif dir == 180 :
            x = x - dist
        elif dir == 270:
            y = y + dist
        new_pos = (x,y)
        if self.map.contains_pos(new_pos):
            return new_pos
        else:
            return None

    def move_to(self, pos):
        if self.map.available_pos(pos) and not pos in self.beacons:
            self.bot.pos = pos
            self.paint()
            return True
        else:
            return False

    def left(self):
        return self.bot.left()

    def right(self):
        return self.bot.right()

    def pickUp(self):
        if self.check(Maze.FRONT, Maze.BEACON):
            front = self.calc_pos(self.bot.pos, self.FRONT, 1)
            self.beacons.remove(front)
            self.bot.beacons.add(front)
            return True
        else:
            return False

    def eatUp(self):
        if self.check(Maze.FRONT, Maze.BEACON):
            front = self.calc_pos(self.bot.pos, self.FRONT, 1)
            self.beacons.remove(front)
            return True
        else:
            return False

    def putDown(self):
        if self.check(Maze.FRONT, Maze.CLEAR) and len(self.bot.beacons) > 0:
            front = self.calc_pos(self.bot.pos, self.FRONT, 1)
            self.bot.beacons.remove(front)
            self.beacons.add(front)
            return True
        else:
            return False

    def paintWhite(self):
        start = True
        if self.bot.paint == self.WHITE:
            start = False
        self.bot.paint = self.WHITE
        self.paint()
        return start

    def paintBlack(self):
        start = True
        if self.bot.paint == self.BLACK:
            start = False
        self.bot.paint = self.BLACK
        self.paint()
        return start

    def stopPainting(self):
        self.bot.paint = self.NOPAINT
        return False

    def paint(self):
        if self.bot.paint == self.BLACK:
            self.paints_white.discard(self.bot.pos)
            self.paints_black.add(self.bot.pos)
        elif self.bot.paint == self.WHITE:
            self.paints_black.discard(self.bot.pos)
            self.paints_white.add(self.bot.pos)

    def check(self, dir, cond):
        pos = self.calc_pos(self.bot.pos, dir, 1)
        if cond == self.CLEAR:
            self.map.available_pos() and not pos in self.beacons
        elif cond == self.BEACON:
            return pos in self.beacons
        elif cond == self.WHITE:
            return pos in self.paints_white
        elif cond == self.BLACK:
            return pos in self.paints_black
        elif cond == self.NOPAINT:
            return pos not in self.paints_white and pos not in self.paints_black
        else:
            return False

    def flipCoin(self):
        return bool(random.getrandbits(1))


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
        self.beacons = set()
        self.paint = None

    def left(self):
        self.dir = dir_left(self.dir)
        return self.dir

    def right(self):
        self.dir = dir_right(self.dir)
        return self.dir






