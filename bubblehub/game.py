from bubblehub.model import GameSpec


class Game:

    def __init__(self, spec: GameSpec):
        self.spec = spec
        self.done = False
        self.timer_tick = 0
        self.max_player_count = 1
        self.max_timer_tick = 1000

    @staticmethod
    def create(spec: GameSpec):
        return Game(spec)

    def player_count(self):
        return self.max_player_count

    def stopped(self):
        return self.done

    def timer(self, now):
        self.timer_tick = self.timer_tick + 1
        if self.timer_tick > self.max_timer_tick:
            self.done = True
