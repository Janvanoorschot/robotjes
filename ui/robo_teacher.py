import json
from gi.repository import Gtk

class RoboTeacherWindow(Gtk.Window):

    def __init__(self):
        self.listeners = []
        Gtk.Window.__init__(self, title="Teacher")
        self.set_default_size(800,600)

        leftbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        rightbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        button1 = Gtk.Button(label="Button1", expand=True)
        button2 = Gtk.Button(label="Button2", expand=True)
        button3 = Gtk.Button(label="Button3", expand=True)
        button4 = Gtk.Button(label="Button4", expand=True)
        leftbox.add(button1)
        leftbox.add(button2)
        rightbox.add(button3)
        rightbox.add(button4)

        grid = Gtk.Grid()
        self.add(grid)
        grid.attach(leftbox, 0, 0, 1, 4)
        grid.attach(rightbox, 1, 0, 4, 4)


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

