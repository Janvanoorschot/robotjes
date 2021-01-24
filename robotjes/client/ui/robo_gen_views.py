from gi.repository import Gtk, Gdk


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
            self.owner.do_signal("EVT_CHANGE_SELECTED_MAZE", self, {
                "name": model.get_value(tree_iter,0),
                "id": model.get_value(tree_iter,1)
            })

    def get_selected_id(self):
        return self.mazes_selected


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
        if len(pathlist) > 0:
            for path in pathlist :
                tree_iter = model.get_iter(path)
                self.games_selected = model.get_value(tree_iter,1)
                self.owner.do_signal("EVT_CHANGE_SELECTED_GAME", self, {
                    "name": model.get_value(tree_iter,0),
                    "id": model.get_value(tree_iter,1)
                })
        else:
            self.owner.do_signal("EVT_CHANGE_SELECTED_GAME", self, None)


    def get_selected_id(self):
        return self.games_selected


class GameComponent(Gtk.Grid):

    def __init__(self, model, owner):
        super().__init__(expand=True, orientation=Gtk.Orientation.VERTICAL)
        self.model = model
        self.game_id = None
        self.owner = owner
        self.players_field = None
        self.scrollable_playerslist = None
        self.players_model = None
        self.players_selection = None
        self.player_selected = None
        self.__construct()

    def __construct(self):
        glabel = Gtk.EventBox()
        glabel.add(Gtk.Label("Game"))
        color = Gdk.color_parse('grey')
        glabel.modify_bg(Gtk.StateType.NORMAL, color)
        self.attach(glabel, 0, 0, 1, 1)
        self.add(Gtk.Label("ticks"))
        self.ticks_field = Gtk.Entry()
        self.add(self.ticks_field)
        self.add(Gtk.Label("status"))
        self.status_field = Gtk.Entry()
        self.add(self.status_field)

        # list of the players
        self.players_field = Gtk.TreeView(expand=True)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Player", renderer, text=0)
        self.players_field.append_column(column)
        self.scrollable_playerslist = Gtk.ScrolledWindow()
        self.scrollable_playerslist.set_vexpand(True)
        self.scrollable_playerslist.add(self.players_field)
        self.players_model = Gtk.ListStore(str,str)
        self.players_field.set_model(self.players_model)
        self.players_selection = self.players_field.get_selection()
        self.players_selection.set_mode(Gtk.SelectionMode.SINGLE)
        self.players_selection.connect("changed", self.selection_changed)
        # self.attach_next_to(self.scrollable_playerslist, glabel, Gtk.PositionType.BOTTOM, 1, 1)
        self.add(self.scrollable_playerslist)

    def set_game(self, game_id):
        self.game_id = game_id
        self.refresh()

    def refresh(self):
        def cb(game_status):
            if "tick" in game_status and "players" in game_status and "status" in game_status:
                self.tick = game_status.get("tick", -1)
                self.isStarted = game_status["status"]["isStarted"]
                self.isStopped = game_status["status"]["isStopped"]
                self.isSuccess = game_status["status"]["isSuccess"]
                self.ticks_field.set_text(str(int(self.tick)))
                statusstr = "/"
                if self.isStarted: statusstr = statusstr + "/started"
                if self.isStopped: statusstr = statusstr + "/stopped"
                if self.isSuccess: statusstr = statusstr + "/success"
                self.status_field.set_text(statusstr)
                player_ids = set()
                for player_spec in game_status["players"]:
                    player_ids.add(player_spec["player_id"])
                    for entry in self.players_model:
                        if entry[1] == player_spec["player_id"]:
                            break
                    else:
                        self.players_model.append([player_spec["player_name"], player_spec["player_id"]])
                for entry in self.players_model:
                    if not entry[1] in player_ids:
                        self.players_model.remove(entry.iter)
        if self.game_id:
            self.model.status_game(self.game_id, cb)
        else:
            pass

    def selection_changed(self, tree_selection):
        (model, pathlist) = tree_selection.get_selected_rows()
        for path in pathlist :
            tree_iter = model.get_iter(path)
            self.player_selected = model.get_value(tree_iter,1)
            self.owner.do_signal("EVT_CHANGE_SELECTED_PLAYER", self, {
                "name": model.get_value(tree_iter,0),
                "id": model.get_value(tree_iter,1)
            })

    def get_selected_id(self):
        return self.player_selected


