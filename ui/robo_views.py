from gi.repository import Gtk, Gdk

class RoboTeacherWindow(Gtk.Window):

    def __init__(self, model):
        self.listeners = []
        Gtk.Window.__init__(self, title="Teacher")
        self.set_default_size(800,600)
        self.model = model
        self.listeners = []

        toppane = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)

        leftbox = Gtk.Grid(expand=True, orientation=Gtk.Orientation.VERTICAL)
        creategame_box = CreateGameComponent(self.model, self)
        leftbox.add(creategame_box)
        games_box = GamesComponent(self.model, self)
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

    def __init__(self, model, owner):
        super().__init__(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.model = model
        self.owner = owner
        self.__construct()

    def __construct(self):
        self.mazes_box = MazesComponent(self.model, self.owner)
        self.add(self.mazes_box)
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

    def on_create_button_clicked(self, button):
        pass

    def on_stop_button_clicked(self, button):
        pass

    def refresh(self):
        pass

    def timer(self):
        pass


class GamesComponent(Gtk.Grid):

    def __init__(self, model, owner):
        super().__init__(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.model = model
        self.owner = owner
        self.__construct()

    def __construct(self):
        glabel = Gtk.EventBox()
        glabel.add(Gtk.Label("Available Games"))
        color = Gdk.color_parse('grey')
        glabel.modify_bg(Gtk.StateType.NORMAL, color)
        self.attach(glabel, 0, 0, 1, 1)

        # list of the games
        self.games_model = get_games_model(self.model)
        self.games_field = Gtk.TreeView(self.games_model, expand=True)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", renderer, text=0)
        self.games_field.append_column(column)
        self.scrollable_gameslist = Gtk.ScrolledWindow()
        self.scrollable_gameslist.set_vexpand(True)
        self.scrollable_gameslist.add(self.games_field)
        self.attach_next_to(self.scrollable_gameslist, glabel, Gtk.PositionType.BOTTOM, 1, 1)

    def refresh(self):
        pass

    def timer(self):
        pass

class MazesComponent(Gtk.Grid):

    def __init__(self, model, owner):
        super().__init__(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.model = model
        self.owner = owner
        self.__construct()

    def __construct(self):
        glabel = Gtk.EventBox()
        glabel.add(Gtk.Label("Available Mazes"))
        color = Gdk.color_parse('grey')
        glabel.modify_bg(Gtk.StateType.NORMAL, color)
        self.attach(glabel, 0, 0, 1, 1)

        self.mazes_model = get_mazes_model(self.model)
        self.mazes_field = Gtk.TreeView(self.mazes_model, expand=True)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", renderer, text=0)
        self.mazes_field.append_column(column)
        self.scrollable_mazeslist = Gtk.ScrolledWindow()
        self.scrollable_mazeslist.set_vexpand(True)
        self.scrollable_mazeslist.add(self.mazes_field)
        self.attach_next_to(self.scrollable_mazeslist, glabel, Gtk.PositionType.BOTTOM, 1, 1)

    def refresh(self):
        pass

    def timer(self):
        pass

def get_games_model(model):
    store = Gtk.ListStore(str, str, float)
    store.append(["game1", "test1", 1.0])
    store.append(["game2", "test2", 2.0])
    store.append(["game3", "test3", 3.0])
    return store

def get_mazes_model(model):
    store = Gtk.ListStore(str, str, float)
    store.append(["maze1", "test1", 1.0])
    store.append(["maze2", "test2", 2.0])
    store.append(["maze3", "test3", 3.0])
    return store
