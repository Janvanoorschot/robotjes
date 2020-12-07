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

    def get_game_status(self, game_id):
        if game_id in self.games:
            return self.games[game_id].game_map()
        else:
            return {}

    def get_game_recording(self, game_id):
        if game_id in self.games:
            return self.games[game_id].game_recording()
        else:
            return {}

    def get_player_status(self, game_id, player_id):
        if game_id in self.games:
            if player_id in self.games[game_id].players:
                return {
                    "game_status": self.games[game_id].game_map(),
                    "player_status": self.games[game_id].player_map(player_id)
                }
            else:
                return {}
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
    """ Contains three pieces of information about a game:
        1. The current game status (from the latest received delta)
        2. The current player status (from the latest received delta)
        3. A list of deltas (a recording?)
    """

    def __init__(self, now, delta):
        """ creation with an initial delta"""
        self.bubble_id = delta['bubble_id']
        self.game_id = delta['game_id']
        self.game_name = delta['game_name']
        self.maze_map = delta['data']['maze_map']
        self.starttime = now
        self.stoptime = None
        self.tick = 0.0
        self.game_tick = 0
        self.isStarted = False
        self.isStopped = False
        self.isSuccess = False
        self.recording = []
        self.players = {}
        self.mapstatus = None
        self.data = {}
        self.update(delta)

    def is_stopped(self):
        return self.stoptime is not None

    def started(self, now, request):
        self.update(request)

    def updated(self, now, request):
        self.update(request)

    def stopped(self, now, request):
        self.update(request)
        self.stoptime = now

    def update(self, delta):
        # {
        #   'bubble_id': 'd0f90888-bd84-48b3-b56e-523433a1e7aa',
        #   'game_id': '93fcc3e6-b696-4cb4-adc2-813cb8ffc37d',
        #   'game_name': 'game2',
        #   'status': {'game_tick': 1,'recording_delta':[], 'isStarted': False, 'isStopped': False, 'isSuccess': False},
        #   'players': [
        #         {
        #             'player_id': 'ba8e8d5c-50e8-4591-9076-aae3d5e40942',
        #             'player_name': 'me',
        #             'player_status': {
        #                   'fog_of_war': {}
        #             }
        #         }
        #   ],
        #   'msg': 'UPDATE',
        #   'tick': 7,
        #   'data': {}
        # }
        self.tick = delta['tick']
        self.game_tick = delta['status']['game_tick']
        self.isStarted = delta['status']['isStarted']
        self.isStopped = delta['status']['isStopped']
        self.isSuccess = delta['status']['isSuccess']
        self.recording.append(delta)
        if len(self.recording) > 10:
            self.recording.pop(0)
        self.players.clear()
        for player in delta['players']:
            self.players[player['player_id']] = player
        self.mapstatus = delta['mapstatus']

    def game_map(self):
        # the extended version of the recording, includes map
        return {
            'game_id': self.game_id,
            'game_name': self.game_name,
            'status': {
                'game_tick': self.game_tick,
                'isStarted': self.isStarted,
                'isStopped': self.isStopped,
                'isSuccess': self.isSuccess
            },
            'recording': self.recording,
            'tick': self.tick,
            'players': list(self.players.keys()),
            'maze_map': self.maze_map
        }

    def game_recording(self):
        #  this should be the delta.
        return {
            'game_id': self.game_id,
            'game_name': self.game_name,
            'status': {
                'game_tick': self.game_tick,
                'isStarted': self.isStarted,
                'isStopped': self.isStopped,
                'isSuccess': self.isSuccess
            },
            'recording': self.recording,
            'tick': self.tick,
            'players': list(self.players.keys()),
            'mapstatus': self.mapstatus
        }

    def player_map(self, player_id):
        if player_id in self.players:
            player = self.players[player_id]
            return {
                'tick': self.tick,
                'game_tick': self.game_tick,
                'player_id': player['player_id'],
                'player_name': player['player_name'],
                'player_status': {
                    'fog_of_war': player['player_status']['fog_of_war']
                }
            }
        else:
            return {}

