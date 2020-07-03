from gi.repository import Gtk, Gdk
from .robo_gen_views import GamesComponent

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

    def on_stop_button_clicked(self, button):
        pass

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
            for entry in self.mazes_model:
                if not entry[1] in mazes:
                    self.mazes_model.remove(entry.iter)
        self.model.list_mazes(cb)

    def selection_changed(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            self.mazes_selected = model.get_value(tree_iter,1)

    def get_selected_id(self):
        return self.mazes_selected
