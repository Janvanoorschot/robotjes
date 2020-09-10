import datetime
import logging
logger = logging.getLogger(__name__)


class StatusKeeper(object):

    def __init__(self):
        self.games = {}
        self.lastseen = {}
        self.now = None
        self.keep_alive = 10
        self.inactive_limit = 10

    def game_status_event(self, request):
        game_id = request['game_id']
        msg = request['msg']
        if game_id not in self.games:
            if msg == 'CREATED':
                game_status = GameStatus(self.now, request)
                self.games[game_id] = game_status
            else:
                logger.warning(f"unexpected message from game: {game_id}")
                return
        now = datetime.datetime.now()
        self.lastseen[game_id] = now
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
        result = {}
        for game_id, game in self.games.items():
            result[game_id] = game.game_name
        return result

    def get_game(self, game_id):
        if game_id in self.games:
            return self.games[game_id].to_map()
        else:
            return {}

    def timer(self, now):
        self.now = now
        for game_id, game in self.games.items():
            # check for 'stopped for long enough'
            if game.is_stopped():
                if (now - game.stoptime).total_seconds() > self.keep_alive:
                    del self.games[game_id]
                    del self.lastseen[game_id]
            # check for 'inactive'
            if game_id in self.lastseen and self.games[game_id].isStarted:
                if (now - self.lastseen[game_id]).total_seconds() > self.inactive_limit:
                    logger.warning(f"inactive game: {game_id}")
                    del self.games[game_id]
                    del self.lastseen[game_id]


class GameStatus(object):

    def __init__(self, now, request):
        self.bubble_id = request['bubble_id']
        self.game_id = request['game_id']
        self.game_name = request['game_name']
        self.starttime = now
        self.stoptime = None
        self.tick = 0.0
        self.isStarted = False
        self.isStopped = False
        self.isSuccess = False
        self.players = []
        self.data = {}

    def is_stopped(self):
        return self.stoptime is not None

    def started(self, now, request):
        self.update(request)

    def updated(self, now, request):
        self.update(request)

    def stopped(self, now, request):
        self.update(request)
        self.stoptime = now

    def update(self, request):
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
        self.tick = request['tick']
        self.isStarted = request['status']['isStarted']
        self.isStopped = request['status']['isStopped']
        self.isSuccess = request['status']['isSuccess']
        self.players = request['players']

    def to_map(self):
        return {
            'game_id': self.game_id,
            'game_name': self.game_name,
            'status': {
                'isStarted': self.isStarted,
                'isStopped': self.isStopped,
                'isSuccess': self.isSuccess
            },
            'tick': self.tick,
            'players': self.players
        }



