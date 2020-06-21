import json
from gi.repository import Gtk

class RoboTeacherWindow(Gtk.Window):

    def __init__(self):
        self.listeners = []
        Gtk.Window.__init__(self, title="Teacher")
        self.set_default_size(800,600)

        leftbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, vexpand=True)
        createbutton = Gtk.Button(label="Create")
        leftbox.add(createbutton )
        stop_button = Gtk.Button(label="Stop")
        leftbox.add(stop_button)
        leftbox.add(Gtk.Label("name"))
        name_field = Gtk.Entry()
        leftbox.add(name_field)
        leftbox.add(Gtk.Label("password"))
        password_field = Gtk.Entry()
        leftbox.add(password_field)

        rightbox = Gtk.Grid()
        view_area = Gtk.GLArea(expand=True)
        teams_area = Gtk.Grid(expand=True)
        rightbox.attach(view_area, 0, 0, 4, 4)
        rightbox.attach(teams_area, 0, 5, 4, 1)

        bottombox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6, hexpand=True)
        info_area = Gtk.Grid(hexpand=True)
        bottombox.add(info_area)
        status_box = Gtk.Entry(hexpand=True)
        info_area.add(status_box)

        grid = Gtk.Grid()
        self.add(grid)
        grid.attach(leftbox, 0, 0, 1, 4)
        grid.attach(rightbox, 1, 0, 4, 4)
        grid.attach(bottombox, 0, 5, 5, 1)

    def add_listener(self, listener):
        self.listeners.append(listener)

    def on_button_clicked(self, widget):
        for listener in self.listeners:
            listener.event("EVT_CREATE_GAME", self)

    def set_text(self, text):
        self.textfield.set_text(text)


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

