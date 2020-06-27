import json

class RoboPlayer():

    """ Controller for the Robomind Player UI """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.game_id = None

    def do_signal(self, etype, sender, *argv):
        if etype == "EVT_CREATE_GAME":
            self.create_game(argv[0])
        else:
            pass

    def timer(self, t):
        self.view.refresh()

    def create_game(self, spec):
        self.model.create_game(self.create_game_cb, spec)

    def create_game_cb(self, reply):
        pass
