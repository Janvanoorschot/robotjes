# semantics.

class Semantics:

    def __init__(self):
        self.opers = {
            "black": self.oper1,
            "white": self.oper1,
            "maxEats": self.oper1,
            "robot": self.oper1,
            "beacon": self.oper1,
            "robotHasBeacon": self.oper1,
        }

    def eval(self, identifier, args, world):
        if identifier in self.opers:
            oper = self.opers[identifier]
            return oper(identifier, args, world)
        else:
            return True

    def oper1(self, identifier, args, world):
        print(f"{identifier}")


ROBO_SEMANTICS = Semantics()