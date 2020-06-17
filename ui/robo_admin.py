import json
from gi.repository import Gtk

class RoboAdminWindow(Gtk.Window):

    def __init__(self):
        self.listeners = []
        Gtk.Window.__init__(self, title="Robo")

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        self.button = Gtk.Button(label="REST")
        self.button.connect("clicked", self.on_button_clicked)
        self.box.pack_start(self.button, True, True, 0)

        self.textfield = Gtk.Label("empty")
        self.box.pack_start(self.textfield, True, True, 0)

    def add_listener(self, listener):
        self.listeners.append(listener)

    def on_button_clicked(self, widget):
        for listener in self.listeners:
            listener.event("EVT_CREATE_GAME", self)

    def set_text(self, text):
        self.textfield.set_text(text)


class RoboAdmin():

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def event(self, etype, sender, *argv):
        if etype == "EVT_CREATE_GAME":
            self.create_game()
        else:
            pass

    def timer(self, t):
        pass

    def create_game(self):
        self.view.set_text("")
        self.model.create_game(self.create_game_cb)

    def create_game_cb(self, j):
        self.view.set_text(json.dumps(j))

