import datetime
import logging
logger = logging.getLogger(__name__)


class StatusKeeper(object):

    def __init__(self):
        self.games = {}
        self.now = None
        self.keep_alive = 10

    def game_status_event(self, request):
        # {
        #   'bubble_id': 'd0f90888-bd84-48b3-b56e-523433a1e7aa',
        #   'game_id': '93fcc3e6-b696-4cb4-adc2-813cb8ffc37d',
        #   'game_name': 'game2',
        #   'status': {'isStarted': False, 'isStopped': False, 'isSuccess': False},
        #   'players': [],
        #   'msg': 'CREATED',
        #   'tick': 1327.285712,
        #   'data': {}
        # }
        game_id = request['game_id']
        msg = request['msg']
        if game_id not in self.games:
            if msg == 'CREATED':
                game_status = GameStatus(self.now, request)
                self.games[game_id] = game_status
            else:
                logger.warning(f"unexpected message from game: {game_id}")
                return
        game = self.games[game_id]
        if msg == 'STARTED':
            game.started(self.now, request)
        elif msg == 'UPDATE':
            game.updated(self.now, request)
        elif msg == 'STOPPED':
            game.stopped(self.now, request)
        elif msg == 'CREATED':
            # CREATED event is already handled
            pass
        elif msg == 'IDLE':
            # IDLE is IDLE
            pass
        else:
            logger.warning(f"unknown msg: {msg}")

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
        self.starttime = now
        self.stoptime = None
        self.game_id = request['game_id']
        self.game_name = request['game_name']

    def is_stopped(self):
        return self.stoptime is not None

    def started(self, now, request):
        pass

    def updated(self, now, request):
        pass

    def stopped(self, now, request):
        pass


