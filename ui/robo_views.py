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
        self.creategame_component = CreateGameComponent(self.model, self)
        leftbox.add(self.creategame_component)
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
        self.creategame_component.refresh()
        self.games_component.refresh()


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
        stop_button = Gtk.Button(label="Stop")
        stop_button.connect("clicked", self.on_stop_button_clicked)
        self.add(stop_button)

    def on_create_button_clicked(self, button):
        name = self.name_field.get_text()
        password = self.name_field.get_text()
        maze_id = self.mazes_component.get_selected_id()
        self.owner.do_signal("EVT_CREATE_GAME", self, {
            "name": name,
            "password": password,
            "maze_id": maze_id
        })

    def on_stop_button_clicked(self, button):
        pass

    def refresh(self):
        self.mazes_component.refresh()


class GamesComponent(Gtk.Grid):

    def __init__(self, model, owner):
        super().__init__(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.model = model
        self.owner = owner
        self.games_field = None
        self.games_model = None
        self.games_selection = None
        self.games_selected = None
        self.__construct()

    def __construct(self):
        glabel = Gtk.EventBox()
        glabel.add(Gtk.Label("Available Games"))
        color = Gdk.color_parse('grey')
        glabel.modify_bg(Gtk.StateType.NORMAL, color)
        self.attach(glabel, 0, 0, 1, 1)

        # list of the games
        self.games_field = Gtk.TreeView(expand=True)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", renderer, text=0)
        self.games_field.append_column(column)
        self.scrollable_gameslist = Gtk.ScrolledWindow()
        self.scrollable_gameslist.set_vexpand(True)
        self.scrollable_gameslist.add(self.games_field)
        self.games_model = Gtk.ListStore(str, str)
        self.games_field.set_model(self.games_model)
        self.games_selection = self.games_field.get_selection()
        self.games_selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.games_selection.connect("changed", self.selection_changed)
        self.attach_next_to(self.scrollable_gameslist, glabel, Gtk.PositionType.BOTTOM, 1, 1)

    def refresh(self):
        def cb(games):
            for game_id, game in games.items():
                for entry in self.games_model:
                    if entry[1] == game_id:
                        break
                else:
                    self.games_model.append([game['id'], game_id])
        self.model.list_games(cb)

    def selection_changed(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            self.games_selected = model.get_value(tree_iter,1)


class MazesComponent(Gtk.Grid):

    def __init__(self, model, owner):
        super().__init__(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.model = model
        self.owner = owner
        self.mazes_field = None
        self.mazes_model = None
        self.mazes_selection = None
        self.mazes_selected = None
        self.__construct()

    def __construct(self):
        glabel = Gtk.EventBox()
        glabel.add(Gtk.Label("Available Mazes"))
        color = Gdk.color_parse('grey')
        glabel.modify_bg(Gtk.StateType.NORMAL, color)
        self.attach(glabel, 0, 0, 1, 1)

        self.mazes_field = Gtk.TreeView(expand=True)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", renderer, text=0)
        self.mazes_field.append_column(column)
        self.scrollable_mazeslist = Gtk.ScrolledWindow()
        self.scrollable_mazeslist.set_vexpand(True)
        self.scrollable_mazeslist.add(self.mazes_field)
        self.mazes_model = Gtk.ListStore(str, str)
        self.mazes_field.set_model(self.mazes_model)
        self.mazes_selection = self.mazes_field.get_selection()
        self.mazes_selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.mazes_selection.connect("changed", self.selection_changed)
        self.attach_next_to(self.scrollable_mazeslist, glabel, Gtk.PositionType.BOTTOM, 1, 1)

    def refresh(self):
        def cb(mazes):
            for maze_id, maze in mazes.items():
                for entry in self.mazes_model:
                    if entry[1] == maze_id:
                        break
                else:
                    self.mazes_model.append([maze['name'], maze_id])
        self.model.list_mazes(cb)

    def selection_changed(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            self.mazes_selected = model.get_value(tree_iter,1)

    def get_selected_id(self):
        return self.mazes_selected


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
