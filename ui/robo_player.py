import uuid

class RoboPlayer():

    """ Controller for the Robomind Player UI """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.game_id = None

    def do_signal(self, etype, sender, *argv):
        if etype == "EVT_REGISTER_PLAYER":
            self.register_player(argv[0])
        else:
            pass

    def timer(self, t):
        self.view.refresh()

    def register_player(self, spec):
        player_name = spec.get("player_name", "Anon")
        password = spec.get("password", "")
        game_id = spec.get("game_id", None)
        directory = spec.get("directory", ".")
        self.model.register_player(self.register_player_cb, {
            "game_id": game_id,
            "player_name": player_name,
            "player_id": str(uuid.uuid4()),
            "password": password
        })

    def register_player_cb(self, reply):
        pass
