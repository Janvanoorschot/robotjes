from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Text, Layout


class UmpireDisplay:
    # controller object
    def __init__(self):
        self.model = UmpireModel()
        self.view = UmpireScreen(self.model)

    def close(self):
        self.view.close()

    def has_key(self):
        return self.view.has_key

    def timer(self):
        if self.view.screen.has_resized():
            self.view.close()
            self.view = UmpireScreen(self.model)
        self.view.timer()

    def game_started(self, game_id, game_name):
        self.model.game_started(game_id, game_name)


    def player_registered(self, player_id, player_name):
        pass


    def player_deregistered(self, player_id):
        pass

    def game_status(self, game_tick, game_status):
        self.model.set_game_status(game_tick, game_status)
        self.view.update(game_tick, 'game')

    def player_status(self, game_tick, player_status):
        self.model.set_player_status(game_tick, player_status)
        self.view.update(game_tick, 'player')


class UmpireModel:
    # model object
    def __init__(self):
        self.game_id = None
        self.game_name = None
        self.game_tick = -1
        self.cur_game_status = None
        self.cur_player_status = None
        self.cur_robo_status = {}

    def game_started(self, game_id, game_name):
        self.game_id = game_id
        self.game_name = game_name

    #   'status': {
    #     'game_tick': 405,
    #     'isStarted': True,
    #     'isStopped': False,
    #     'isSuccess': True
    #   }
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


class UmpireScreen:
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
            self.player_view,
        ]
        self.scenes.append(Scene(self.effects, -1))
        self.screen.set_scenes(self.scenes)

    def update(self, game_tick, type, *args):
        if type == 'game':
            self.game_view.upd(args)
        elif type == 'player':
            self.player_view.upd(args)
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
                                       screen.height * 1 // 3,
                                       screen.width * 1 // 2,
                                       x=0,
                                       y=0,
                                       on_load=self.upd,
                                       hover_focus=True,
                                       title="Game")
        self.model = model
        self.gameid_field = Text("", "gameid")
        self.gamename_field = Text("", "gamename")
        self.gametick_field = Text("", "gametick")
        layout = Layout([4,1,1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self.gameid_field, 0)
        layout.add_widget(self.gamename_field, 1)
        layout.add_widget(self.gametick_field, 2)
        self.set_theme('monochrome')
        self.fix()

    def upd(self, *args):
        if self.model.cur_game_status:
            self.gameid_field.value = self.model.game_id
            self.gamename_field.value = self.model.game_name
            self.gametick_field.value = str(self.model.cur_game_status['game_tick'])


class PlayerView(Frame):

    def __init__(self, screen, model):
        super(PlayerView, self).__init__(screen,
                                       screen.height * 1 // 3,
                                       screen.width * 1 // 2,
                                       x=screen.width//2,
                                       y=0,
                                       on_load=self.upd,
                                       hover_focus=True,
                                       title="Player")
        self.model = model
        self.playerid_field = Text("", "playerid")
        self.playername_field = Text("", "playername")
        layout = Layout([1,1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self.playerid_field, 0)
        layout.add_widget(self.playername_field, 1)
        self.set_theme('monochrome')
        self.fix()

    def upd(self, *args):
        if self.model.cur_player_status:
            self.playerid_field.value = self.model.cur_player_status['player_id']
            self.playername_field.value = self.model.cur_player_status['player_name']
