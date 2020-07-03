from bubblehub.model import GameSpec


class Game:

    def __init__(self, spec: GameSpec):
        self.spec = spec
        self.done = False
        self.success = False
        self.timer_tick = 0
        self.max_player_count = 1
        self.max_start_tick = 15
        self.max_timer_tick = 1000

    def created(self):
        pass

    def started(self, players):
        pass

    def stopped(self):
        return self.done

    def player_count(self):
        return self.max_player_count

    def timer(self, now):
        self.timer_tick = self.timer_tick + 1
        if self.timer_tick > self.max_start_tick:
            self.done = True
            self.success = False
        elif self.timer_tick > self.max_timer_tick:
            self.done = True
            self.success = True

    def result(self):
        return self.success
