import json

class RoboTeacher():

    """ Controller for the Robomind Teacher UI """

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.game_id = None

    def event(self, etype, sender, *argv):
        if etype == "EVT_CREATE_GAME":
            self.create_game()
        else:
            pass

    def timer(self, t):
        self.view.refresh()
        # self.model.list_games(self.list_games_db)
        if self.game_id:
            self.model.get_game(self.game_id, self.status_game_db)

    def create_game(self):
        self.view.set_text("")
        self.model.create_game(self.create_game_cb)

    def create_game_cb(self, j):
        self.game_id = j["game_id"]
        self.view.set_text(json.dumps(j))
