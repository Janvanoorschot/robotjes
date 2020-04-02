# semantics.

class Semantics:

    def __init__(self):
        self.opers = {
            "robot": self.oper1,
            "beacon": self.oper1,
            "black": self.oper1,
            "white": self.oper1,
            "maxEats": self.oper1,
            "robotHasBeacon": self.oper1,
            "minWhitePaintUsed": self.oper1,
        }

    def eval(self, identifier, args, world):
        if identifier in self.opers:
            oper = self.opers[identifier]
            return oper(identifier, args, world)
        else:
            print(f"unknown {identifier}")
            return True

    def oper1(self, identifier, args, world):
        print(f"known {identifier}")
        return True


ROBO_SEMANTICS = Semantics()