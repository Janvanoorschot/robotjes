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
        self.registerplayer_component = RegisterPlayerComponent(self.model, self)
        leftbox.add(self.registerplayer_component)
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
        pass

    def refresh(self):
        self.registerplayer_component.refresh()


class RegisterPlayerComponent(Gtk.Grid):

    def __init__(self, model, owner):
        super().__init__(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.model = model
        self.owner = owner
        self.__construct()

    def __construct(self):
        self.add(Gtk.Label("name"))
        self.name_field = Gtk.Entry()
        self.add(self.name_field)
        self.dir_chooser = DirectorySelectorComponent(self)
        self.add(self.dir_chooser)
        self.games_component = GamesComponent(self.model, self)
        self.add(self.games_component)
        self.add(Gtk.Label("password"))
        self.password_field = Gtk.Entry()
        self.add(self.password_field)
        create_button = Gtk.Button(label="Register")
        create_button.connect("clicked", self.on_register_button_clicked)
        self.add(create_button )

    def on_register_button_clicked(self, button):
        name = self.name_field.get_text()
        password = self.password_field.get_text()
        game_id = self.games_component.get_selected_id()
        directory = self.dir_chooser.get_current_folder()
        self.owner.do_signal("EVT_REGISTER_PLAYER", self, {
            "game_id": game_id,
            "player_name": name,
            "password": password,
            "directory": directory
        })

    def refresh(self):
        self.games_component.refresh()


class DirectorySelectorComponent(Gtk.Box):

    def __init__(self, owner):
        super().__init__(expand=True, orientation=Gtk.Orientation.HORIZONTAL)
        self.owner = owner
        self.__construct()

    def __construct(self):
        self.button = Gtk.FileChooserButton(action=Gtk.FileChooserAction.SELECT_FOLDER)
        self.add(self.button)

    def get_current_folder(self):
        return self.button.get_current_folder()


