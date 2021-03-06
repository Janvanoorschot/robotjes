import random
from .map import Map

class World(object):

    # directions
    LEFT = 90
    FRONT = 0
    RIGHT = 270
    BACK = 180

    # status of position
    CLEAR = "clear"
    OBSTACLE = "obstacle"
    BEACON = "beacon"
    WHITE = "white"
    BLACK = "black"
    NOPAINT = "nopaint"
    ROBOT = "robot"

    def __init__(self, map):
        self.map = map
        self.paints_black = set(self.map.paints_blacks())
        self.paints_white = set(self.map.paints_whites())
        self.beacons = set(self.map.start_beacons())
        start_positions = self.map.start_positions()
        self.bot = Bot(start_positions[0], 90)
        self.profile = {
            "paintWhites": 0,
            "paintBlacks": 0,
            "whitePaintUsed": 0,
            "blackPaintUsed": 0,
            "robotHasBumped": 0,
            "scriptTotalCharacters": 0,
            "scriptCharacters": 0,
            "scriptCalls": 0,
            "scriptBasicCommands": 0,
            "see": 0,
            "flipCoins": 0,
            "robotHasBeacon": 0,
            "exploredTileCount": 0,
            "scriptRecursive": 0,
            "successfulGets": 0,
            "robotOrientation": 0,
            "gets": 0,
            "puts": 0,
            "eats": 0,
            "successfulEats": 0,
            "moves": 0,
            "explored": 0,
            "robotActions": 0,
            "robotX": 0,
            "robotY": 0,
            "successfulPuts": 0,
            "total": 0,
        }

    def inc(self, name, count=1):
        if(name in self.profile):
            self.profile[name] = self.profile[name] + count

    def available_pos(self, pos):
        return self.map.available_pos(pos) and not pos in self.beacons and pos != self.bot.pos

    def calc_pos(self, bot, viewdir, dist):
        pos = bot.pos
        dir = dir_add(bot.dir,viewdir)
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
        self.inc("gets")
        if self.check(World.FRONT, World.BEACON):
            front = self.calc_pos(self.bot, self.FRONT, 1)
            self.beacons.remove(front)
            self.bot.beacons.add(front)
            return True
        else:
            return False

    def eatUp(self):
        self.inc("eats")
        if self.check(World.FRONT, World.BEACON):
            front = self.calc_pos(self.bot, self.FRONT, 1)
            self.beacons.remove(front)
            self.inc("successfulEats")
            return True
        else:
            return False

    def putDown(self):
        self.inc("puts")
        if self.check(World.FRONT, World.CLEAR) and len(self.bot.beacons) > 0:
            front = self.calc_pos(self.bot, self.FRONT, 1)
            self.bot.beacons.pop()
            self.beacons.add(front)
            self.inc("successfulPuts     ")
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
            if self.bot.pos in self.paints_white:
                self.inc("paintWhites", -1)
                self.paints_white.discard(self.bot.pos)
            self.paints_black.add(self.bot.pos)
            self.inc("blackPaintUsed")
            self.inc("paintBlacks")
        elif self.bot.paint == self.WHITE:
            if self.bot.pos in self.paints_black:
                self.inc("paintBlacks", -1)
                self.paints_black.discard(self.bot.pos)
            self.paints_white.add(self.bot.pos)
            self.inc("whitePaintUsed")
            self.inc("paintWhites")

    def check(self, dir, cond):
        pos = self.calc_pos(self.bot, dir, 1)
        return self.check_pos(pos, cond)

    def check_pos(self, pos, cond):
        if cond == self.CLEAR:
            return self.map.available_pos(pos) and not pos in self.beacons
        elif cond == self.OBSTACLE:
            return not self.map.available_pos(pos) or pos in self.beacons
        elif cond == self.BEACON:
            return pos in self.beacons
        elif cond == self.ROBOT:
            return pos == self.bot.pos
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


def dir_add(dir1, dir2):
    if not dir1 in DIRS or not dir2 in DIRS:
        raise ValueError(f"invalid direction {dir1}/{dir2}")
    return (dir1 + dir2) % 360


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






