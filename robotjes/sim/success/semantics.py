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
            "maxEats": self.true,
            "robotHasBeacon": self.robotHasBeacon,
            "minWhitePaintUsed": self.true,
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

    def robotHasBeacon(self, identifier, args, world):
        return len(world.bot.beacons) > 0

    def true(self, identifier, args, world):
        print(f"known {identifier}")
        return True




ROBO_SEMANTICS = Semantics()