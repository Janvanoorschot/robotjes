from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Text, Layout


class PlayerScreen:

    def __init__(self):
        self.cur_game_status = None
        self.cur_player_status = None
        self.cur_robo_status = None
        self.screen = Screen.open()
        self.game_view = GameView(self.screen, self)
        self.player_view = PlayerView(self.screen, self)
        self.scenes = []
        self.effects = [
            self.game_view,
            self.player_view
        ]
        self.scenes.append(Scene(self.effects, -1))
        self.screen.set_scenes(self.scenes)

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
        self.cur_game_status = game_status
        self.game_view.reload()

    # {
    #   'player_id': 'd6e023e8-8adb-4482-a07e-8f8e1328a3da',
    #   'robos': ...
    # }
    def player_status(self, game_tick, player_status):
        self.cur_player_status = player_status
        self.player_view.reload()

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
        self.cur_robo_status = robo_status


class GameView(Frame):

    def __init__(self, screen, model):
        super(GameView, self).__init__(screen,
                                       screen.height * 1 // 6,
                                       screen.width * 1 // 3,
                                       x=0,
                                       y=0,
                                       on_load=self.reload,
                                       hover_focus=False,
                                       title="Game")
        self.model = model
        self.gameid_field = Text("", "gameid")
        self.gamename_field = Text("", "gamename")
        self.gametick_field = Text("", "gametick")
        layout = Layout([1,1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self.gameid_field)
        layout.add_widget(self.gamename_field)
        layout.add_widget(self.gametick_field)
        self.set_theme('monochrome')
        self.fix()

    def reload(self):
        if self.model.cur_game_status:
            self.gameid_field.value = self.model.cur_game_status['game_id']
            self.gamename_field.value = self.model.cur_game_status['game_name']
            self.gametick_field.value = str(self.model.cur_game_status['status']['game_tick'])


class PlayerView(Frame):

    def __init__(self, screen, model):
        super(PlayerView, self).__init__(screen,
                                       screen.height * 1 // 6,
                                       screen.width * 1 // 3,
                                        y=0,
                                       on_load=self.reload,
                                       hover_focus=False,
                                       title="Player")
        self.model = model
        self.playerid_field = Text("", "playerid")
        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self.playerid_field)
        self.set_theme('monochrome')
        self.fix()

    def reload(self):
        if self.model.cur_game_status:
            self.playerid_field.value = self.model.cur_player_status['player_id']


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
class RoboView(Frame):

    def __init__(self, screen, model):
        super(RoboView, self).__init__(screen,
                                       screen.height * 1 // 6,
                                       screen.width * 1 // 3,
                                        y=0,
                                       on_load=self.reload,
                                       hover_focus=False,
                                       title="Player")
        self.model = model
        self.playerid_field = Text("", "playerid")
        layout = Layout([1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self.playerid_field)
        self.set_theme('monochrome')
        self.fix()

    def reload(self):
        if self.model.cur_game_status:
            self.playerid_field.value = self.model.cur_player_status['player_id']


