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

    # {
    #   'game_id': '240cc20b-96f5-4b61-b88e-06f930006c6c',
    #   'game_name': 'the_game',
    #   'status': {
    #     'game_tick': 405,
    #     'isStarted': True,
    #     'isStopped': False,
    #     'isSuccess': True
    #   }
    # }
    def game_status(self, game_tick, game_status):
        pass

    # {
    #   'player_id': 'd6e023e8-8adb-4482-a07e-8f8e1328a3da',
    #   'robos': ...
    # }
    def player_status(self, game_tick, player_status):
        pass

    # {
    #    'pos': [7, 11],
    #    'load': 0,
    #    'dir': 180,
    #    'recording': [
    #      [304, 'forward', [1], True],
    #      [305, 'right', [1], True],
    #      [306, 'forward', [1], True]],
    #    'fog_of_war': {
    #      'left': [None, None, None, False],
    #      'front': [None, None, None, False],
    #      'right': [None, None, None, False]
    #    }
    # }
    def robo_status(self, game_tick, robo_id, robo_status):
        pass



