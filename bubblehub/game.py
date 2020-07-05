from bubblehub.model import GameSpec


class Game:

    def __init__(self, owner, spec: GameSpec):
        self.owner = owner
        self.spec = spec
        self.started = False
        self.stopped = False
        self.success = False
        self.timer_tick = 0
        self.max_player_count = 1
        self.max_start_tick = 15
        self.max_timer_tick = 1000
        self.players = []

    def created(self):
        pass

    def started(self, players):
        self.players = players

    def stopped(self):
        return self.stopped

    def player_count(self):
        return self.max_player_count

    def status_update(self):
        self.owner.publish('STATUS',{})

    def timer(self, now):
        self.timer_tick = self.timer_tick + 1
        if len(self.players) < self.max_player_count and self.timer_tick > self.max_start_tick:
            self.stopped = True
            self.success = False
        elif self.timer_tick > self.max_timer_tick:
            self.stopped = True
            self.success = True
        if not self.stopped:
            self.status_update()

    def result(self):
        return self.success
