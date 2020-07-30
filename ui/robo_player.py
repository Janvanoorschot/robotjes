import uuid

class RoboPlayer():

    """ Controller for the Robomind Player UI """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.game_id = None
        self.player_id = None

    def do_signal(self, etype, sender, *argv):
        if etype == "EVT_REGISTER_PLAYER":
            self.register_player(argv[0])
        else:
            pass

    def timer(self, t):
        if self.player_id and self.game_id:
            self.model.player_move(self.player_move_cb, self.game_id, self.player_id, {"aap": "noot"})
        self.view.refresh()

    def register_player(self, spec):
        player_name = spec.get("player_name", "Anon")
        password = spec.get("password", "")
        self.game_id = spec.get("game_id", None)
        self.player_id = str(uuid.uuid4())
        directory = spec.get("directory", ".")
        self.model.register_player(self.register_player_cb, {
            "game_id": self.game_id,
            "player_id": self.player_id,
            "player_name": player_name,
            "game_password": password
        })

    def register_player_cb(self, reply):
        pass

    def player_move_cb(self, reply):
        pass
