from gi.repository import Gtk, Gdk


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
        self.games_model = Gtk.ListStore(str,str)
        self.games_field.set_model(self.games_model)
        self.games_selection = self.games_field.get_selection()
        self.games_selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.games_selection.connect("changed", self.selection_changed)
        self.attach_next_to(self.scrollable_gameslist, glabel, Gtk.PositionType.BOTTOM, 1, 1)

    def refresh(self):
        def cb(games):
            for game_id, game_name in games.items():
                for entry in self.games_model:
                    if entry[1] == game_id:
                        break
                else:
                    self.games_model.append([game_name, game_id])
            for entry in self.games_model:
                if not entry[1] in games:
                    self.games_model.remove(entry.iter)
        self.model.list_games(cb)

    def selection_changed(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            self.games_selected = model.get_value(tree_iter,1)

    def get_selected_id(self):
        return self.games_selected


class GameComponent(Gtk.Grid):

    def __init__(self, model, game_id, owner):
        super().__init__(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.model = model
        self.game_id = game_id
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
        self.games_model = Gtk.ListStore(str,str)
        self.games_field.set_model(self.games_model)
        self.games_selection = self.games_field.get_selection()
        self.games_selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.games_selection.connect("changed", self.selection_changed)
        self.attach_next_to(self.scrollable_gameslist, glabel, Gtk.PositionType.BOTTOM, 1, 1)

    def refresh(self):
        def cb(games):
            for game_id, game_name in games.items():
                for entry in self.games_model:
                    if entry[1] == game_id:
                        break
                else:
                    self.games_model.append([game_name, game_id])
            for entry in self.games_model:
                if not entry[1] in games:
                    self.games_model.remove(entry.iter)
        self.model.list_games(cb)

    def selection_changed(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            self.games_selected = model.get_value(tree_iter,1)

    def get_selected_id(self):
        return self.games_selected


