
class StatusKeeper(object):

    def __init__(self):
        self.games = {}

    def game_status_event(self, request):
        bubble_id = request['bubble']
        game_id = request['game']
        if game_id not in self.games:
            game_status = GameStatus(game_id)


class GameStatus(object):

    def __init__(self):
        pass