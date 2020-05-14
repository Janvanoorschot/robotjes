from gi.repository import Gtk

class RoboMainWindow(Gtk.Window):

    def __init__(self, requestor):
        self.requestor = requestor
        Gtk.Window.__init__(self, title="Robo")

        self.button = Gtk.Button(label="REST")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        self.requestor.list_bubbles()
