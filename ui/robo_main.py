import json
from gi.repository import Gtk

class RoboMainWindow(Gtk.Window):

    def __init__(self, requestor):
        self.requestor = requestor
        Gtk.Window.__init__(self, title="Robo")

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        self.button = Gtk.Button(label="REST")
        self.button.connect("clicked", self.on_button_clicked)
        self.box.pack_start(self.button, True, True, 0)

        self.textfield = Gtk.Label("empty")
        self.box.pack_start(self.textfield, True, True, 0)

    def on_button_clicked(self, widget):
        self.textfield.set_text("")
        self.requestor.list_bubbles(self.my_cb)


    def my_cb(self, j):
        self.textfield.set_text(json.dumps(j))
