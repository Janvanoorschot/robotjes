from gi.repository import Gtk, Gdk
from .robo_gen_views import GamesComponent

class RoboPlayerWindow(Gtk.Window):

    def __init__(self, model):
        self.listeners = []
        Gtk.Window.__init__(self, title="Player")
        self.set_default_size(800,600)
        self.model = model
        self.listeners = []

        toppane = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)

        leftbox = Gtk.Grid(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.games_component = GamesComponent(self.model, self)
        leftbox.add(self.games_component)
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

    def do_signal(self, etype, sender, *argv):
        for listener in self.listeners:
            listener.do_signal(etype, self, *argv)

    def set_text(self, text):
        self.textfield.set_text(text)

    def refresh(self):
        self.games_component.refresh()


