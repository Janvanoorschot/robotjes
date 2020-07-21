import datetime
import logging
logger = logging.getLogger(__name__)


class StatusKeeper(object):

    def __init__(self):
        self.starttime = datetime.datetime.now()
        self.now = self.starttime
        self.stoptime = None
        self.games = {}
        self.keep_alive = 10

    def game_status_event(self, request):
        bubble_id = request['bubble_id']
        game_id = request['game_id']
        if game_id not in self.games:
            if request['msg'] == 'CREATED':
                game_status = GameStatus(self.now, request)
                self.games[game_id] = game_status
            else:
                logger.warning(f"unexpected message from game: {game_id}")
                return
        game = self.games[game_id]
        if request['msg'] == 'CREATED':
            pass
        elif request['msg'] == 'STATUS':
            pass
        elif request['msg'] == 'STOPPED':
            game.stop(self.now)
        else:
            logger.warning(f"unknown msg: {request['msg']}")

    def list_games(self):
        return self.games

    def timer(self, now):
        self.now = now
        for game_id, game in self.games.items():
            if game.is_stopped():
                if (now - game.stoptime).total_seconds() > self.keep_alive:
                    del self.games[game_id]



class GameStatus(object):

    def __init__(self, now, request):
        self.game_id = request['game_id']
        self.game_name = request['game_name']
        self.starttime = now
        self.stoptime = None

    def stop(self, now):
        self.stoptime = now

    def is_stopped(self):
        return self.stoptime != None


