import json
from gi.repository import Gtk, Gdk

class RoboTeacherWindow(Gtk.Window):

    def __init__(self):
        self.listeners = []
        Gtk.Window.__init__(self, title="Teacher")
        self.set_default_size(800,600)
        self.model = None
        self.controller = None

        toppane = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)

        leftbox = Gtk.Grid(expand=True, orientation=Gtk.Orientation.VERTICAL)
        creategame_box = CreateGameComponent(self.model, self.controller)
        leftbox.add(creategame_box)
        games_box = GamesComponent(self.model, self.controller)
        leftbox.add(games_box)

        rightbox = Gtk.Grid()
        view_area = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        teams_area = Gtk.Grid(expand=True)
        rightbox.attach(view_area, 0, 0, 4, 4)
        rightbox.attach(teams_area, 0, 5, 4, 1)

        toppane.add1(leftbox)
        toppane.add2(rightbox)

        bottombox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6, hexpand=True)
        info_area = Gtk.Grid(hexpand=True, )
        bottombox.add(info_area)
        status_box = Gtk.Entry(hexpand=True)
        info_area.add(status_box)

        grid = Gtk.Grid(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.add(grid)
        grid.add(toppane)
        grid.add(bottombox)

    def add_listener(self, listener):
        self.listeners.append(listener)

    def on_button_clicked(self, widget):
        for listener in self.listeners:
            listener.event("EVT_CREATE_GAME", self)

    def set_text(self, text):
        self.textfield.set_text(text)


class CreateGameComponent(Gtk.Grid):

    def __init__(self, model, controller):
        super().__init__(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.model = model
        self.controller = controller
        self.__construct()

    def __construct(self):
         self.add(Gtk.Label("name"))
         self.name_field = Gtk.Entry()
         self.add(self.name_field)
         self.add(Gtk.Label("password"))
         self.password_field = Gtk.Entry()
         self.add(self.password_field)
         create_button = Gtk.Button(label="Create")
         create_button.connect("clicked", self.on_create_button_clicked)
         self.add(create_button )
         stop_button = Gtk.Button(label="Stop")
         stop_button.connect("clicked", self.on_stop_button_clicked)
         self.add(stop_button)

    def on_create_button_clicked(self):
        pass

    def on_stop_button_clicked(self):
        pass

    def refresh(self):
        pass

    def timer(self):
        pass


class GamesComponent(Gtk.Grid):

    def __init__(self, model, controller):
        super().__init__(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.model = model
        self.controller = controller
        self.__construct()

    def __construct(self):
        glabel = Gtk.EventBox()
        glabel.add(Gtk.Label("games"))
        color = Gdk.color_parse('grey')
        glabel.modify_bg(Gtk.StateType.NORMAL, color)
        self.attach(glabel, 0, 0, 1, 1)
        self.games_field = Gtk.ListBox(expand=True)
        self.attach_next_to(self.games_field, glabel, Gtk.PositionType.BOTTOM, 1, 1)

    def refresh(self):
        pass

    def timer(self):
        pass

class RoboTeacher():

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.game_id = None

    def event(self, etype, sender, *argv):
        if etype == "EVT_CREATE_GAME":
            self.create_game()
        else:
            pass

    def timer(self, t):
        # self.model.list_games(self.list_games_db)
        if self.game_id:
            self.model.status_game(self.game_id, self.status_game_db)

    def create_game(self):
        self.view.set_text("")
        self.model.create_game(self.create_game_cb)

    def create_game_cb(self, j):
        self.game_id = j["game_id"]
        self.view.set_text(json.dumps(j))

    def list_games_db(self, j):
        self.view.set_text(json.dumps(j))

    def status_game_db(self, j):
        status = j["status"]["status"]["status"]
        if status == "IDLE":
            self.game_id = None
            self.view.set_text(json.dumps(j))
        else:
            self.view.set_text(json.dumps(j))

