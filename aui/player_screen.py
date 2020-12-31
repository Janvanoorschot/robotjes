from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Text, Layout

class PlayerDisplay:
    # controller object
    def __init__(self):
        self.model = PlayerModel()
        self.view = PlayerScreen(self.model)

    def close(self):
        self.view.close()

    def has_key(self):
        return self.view.has_key

    def timer(self):
        if self.view.screen.has_resized():
            self.view.close()
            self.view = PlayerScreen(self.model)
        self.view.timer()

    def game_status(self, game_tick, game_status):
        self.model.set_game_status(game_tick, game_status)
        self.view.update(game_tick, 'game')

    def player_status(self, game_tick, player_status):
        self.model.set_player_status(game_tick, player_status)
        self.view.update(game_tick, 'player')

    def robo_status(self, game_tick, robo_id, robo_status):
        self.model.set_robo_status(game_tick, robo_id, robo_status)
        self.view.update(game_tick, 'robo', robo_id)


class PlayerModel:
    # model object
    def __init__(self):
        self.game_tick = -1
        self.cur_game_status = None
        self.cur_player_status = None
        self.cur_robo_status = {}

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
    def set_game_status(self, game_tick, game_status):
        self.game_tick = game_tick
        self.cur_game_status = game_status

    # {
    #   'player_id': 'd6e023e8-8adb-4482-a07e-8f8e1328a3da',
    #   'robos': ...
    # }
    def set_player_status(self, game_tick, player_status):
        self.game_tick = game_tick
        self.cur_player_status = player_status

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
    def set_robo_status(self, game_tick, robo_id, robo_status):
        self.game_tick = game_tick
        self.cur_robo_status[robo_id] = robo_status


class PlayerScreen:
    # main screen/view/windows object
    def __init__(self, model):
        self.model = model
        self.last_event = None
        self.has_key = False
        Screen.wrapper(self.populate, catch_interrupt=True)

    def populate(self, screen):
        self.screen = screen
        self.game_view = GameView(self.screen, self.model)
        self.player_view = PlayerView(self.screen, self.model)
        self.scenes = []
        self.effects = [
            self.game_view,
            self.player_view
        ]
        self.scenes.append(Scene(self.effects, -1))
        self.screen.set_scenes(self.scenes)

    def update(self, game_tick, type, *args):
        if type == 'game':
            self.game_view.reload()
        elif type == 'player':
            self.player_view.reload()
        else:
            pass

    def close(self):
        self.screen.close()

    def timer(self):
        self.last_event = self.screen.get_event()
        if not self.has_key and self.last_event:
            self.has_key = True
        self.screen.draw_next_frame()


class GameView(Frame):

    def __init__(self, screen, model):
        super(GameView, self).__init__(screen,
                                       screen.height * 1 // 6,
                                       screen.width * 1 // 3,
                                       x=0,
                                       y=0,
                                       on_load=self.reload,
                                       hover_focus=True,
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
                                       hover_focus=True,
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


