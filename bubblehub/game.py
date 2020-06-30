from bubblehub.model import GameSpec


class Game:

    def __init__(self, spec: GameSpec):
        self.spec = spec

    @staticmethod
    def create(spec: GameSpec):
        return Game(spec)

    def player_count(self):
        return 1