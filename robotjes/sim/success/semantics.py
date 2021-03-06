# semantics.

class Semantics:

    def __init__(self):
        self.opers = {
            "clear": self.check,
            "obstacle": self.check,
            "beacon": self.check,
            "white": self.check,
            "black": self.check,
            "nopaint": self.check,
            "robot": self.check,
            "maxEats": self.maxEats,
            "robotHasBeacon": self.robotHasBeacon,
            "minWhitePaintUsed": self.minWhitePaintUsed,
            "minBlackPaintUsed": self.minBlackPaintUsed,
        }

    def eval(self, identifier, args, world):
        if identifier in self.opers:
            oper = self.opers[identifier]
            return oper(identifier, args, world)
        else:
            print(f"unknown {identifier}")
            return True

    def check(self, identifier, args, world):
        # note that the identifier name need to match the constants defined in world.py
        if len(args) < 2:
            return False
        pos = (args[0], args[1])
        return world.check_pos(pos, identifier)

    def maxEats(self, identifier, args, world):
        if len(args) != 1:
            return False
        return world.profile["eats"] < args[0]

    def robotHasBeacon(self, identifier, args, world):
        return len(world.bot.beacons) > 0

    def minWhitePaintUsed(self, identifier, args, world):
        if len(args) != 1:
            return False
        return world.profile["whitePaintUsed"] >= args[0]

    def minBlackPaintUsed(self, identifier, args, world):
        if len(args) != 1:
            return False
        return world.profile["blackPaintUsed"] >= args[0]

    def true(self, identifier, args, world):
        print(f"unimplemented identifier: {identifier}")
        return True

ROBO_SEMANTICS = Semantics()