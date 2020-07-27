from gi.repository import Gtk, Gdk
from .robo_gen_views import GamesComponent, MazesComponent, GameComponent

class RoboUmpireWindow(Gtk.Window):

    def __init__(self, model):
        self.listeners = []
        Gtk.Window.__init__(self, title="Umpire")
        self.set_default_size(800,600)
        self.model = model
        self.listeners = []

        toppane = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)

        leftbox = Gtk.Grid(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.creategame_component = CreateGameComponent(self.model, self)
        leftbox.add(self.creategame_component)
        self.games_component = GamesComponent(self.model, self)
        leftbox.add(self.games_component)
        stop_button = Gtk.Button(label="Stop")
        stop_button.connect("clicked", self.on_stop_button_clicked)
        leftbox.add(stop_button)

        rightbox = Gtk.Grid(expand=True, orientation=Gtk.Orientation.VERTICAL)
        view_area = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        self.game_component = GameComponent(self.model, self)
        # teams_area = Gtk.Grid(expand=True)
        rightbox.attach(view_area, 0, 0, 4, 4)
        rightbox.attach(self.game_component, 0, 5, 4, 1)

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
        if etype == "EVT_CHANGE_SELECTED_GAME":
            game_id = argv[0]["id"]
            game_name = argv[0]["name"]
            self.game_component.set_game(game_id)
        else:
            for listener in self.listeners:
                listener.do_signal(etype, self, *argv)

    def on_stop_button_clicked(self, button):
        pass

    def refresh(self):
        self.creategame_component.refresh()
        self.games_component.refresh()
        self.game_component.refresh()


class CreateGameComponent(Gtk.Grid):

    def __init__(self, model, owner):
        super().__init__(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.model = model
        self.owner = owner
        self.__construct()

    def __construct(self):
        self.mazes_component = MazesComponent(self.model, self.owner)
        self.add(self.mazes_component)
        self.add(Gtk.Label("name"))
        self.name_field = Gtk.Entry()
        self.add(self.name_field)
        self.add(Gtk.Label("password"))
        self.password_field = Gtk.Entry()
        self.add(self.password_field)
        create_button = Gtk.Button(label="Create")
        create_button.connect("clicked", self.on_create_button_clicked)
        self.add(create_button )

    def on_create_button_clicked(self, button):
        name = self.name_field.get_text()
        password = self.password_field.get_text()
        maze_id = self.mazes_component.get_selected_id()
        self.owner.do_signal("EVT_CREATE_GAME", self, {
            "name": name,
            "password": password,
            "maze_id": maze_id
        })

    def refresh(self):
        self.mazes_component.refresh()
