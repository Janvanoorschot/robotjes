import uuid

class RoboUmpire():

    """ Controller for the Robomind Umpire UI """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.umpire_id = str(uuid.uuid4())
        self.game_id = None

    def do_signal(self, etype, sender, *argv):
        if etype == "EVT_CREATE_GAME":
            self.create_game(argv[0])
        elif etype == "EVT_STOP_GAME":
            self.stop_game(argv[0])
        elif etype == "EVT_CHANGE_SELECTED_MAZE":
            pass
        elif etype == "EVT_CHANGE_SELECTED_GAME":
            pass
        else:
            pass

    def timer(self, t):
        self.view.refresh()

    def create_game(self, args):
        spec = {
            "umpire_id": self.umpire_id,
            "game_name": args["name"],
            "game_password": args["password"],
            "maze_id": args["maze_id"]
        }
        self.model.create_game(self.dummy_cb, spec)

    def stop_game(self, args):
        spec = {
            "umpire_id": self.umpire_id,
            "game_id": args["game_id"]
        }
        self.model.stop_game(self.dummy_cb, spec)

    def dummy_cb(self, reply):
        pass
