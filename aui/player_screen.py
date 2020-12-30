from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen

class PlayerScreen:

    def __init__(self):
        self.screen = None
        self.populate()

    def populate(self):
        # create screen
        self.screen = Screen.open()
        effects = [
            Cycle(
                self.screen,
                FigletText("ASCIIMATICS", font='big'),
                self.screen.height // 2 - 8),
            Cycle(
                self.screen,
                FigletText("ROCKS!", font='big'),
                self.screen.height // 2 + 3),
            Stars(self.screen, (self.screen.width + self.screen.height) // 2)
        ]
        self.screen.set_scenes([Scene(effects, 500)])

    def close(self):
        self.screen.close()

    def timer(self):
        self.screen.draw_next_frame()

    def game_status(self, game_tick, game_status):
        pass

    def player_status(self, game_tick, player_status):
        pass

    def robo_status(self, game_tick, robo_id, robo_status):
        pass



