import collections
from . import CLIRequestor
import asyncio


class CLIUmpire():

    def __init__(self, loop, url, client):
        self.requestor = CLIRequestor(loop, url)
        self.client = client
        self.game_id = None
        self.game_tick = None
        self.success = False
        self.started = False
        self.stopped = False
        self.lock = asyncio.Lock()
        self.players = {}

    async def run_game(self, umpire, name, password, maze):
        """ Validate the params, create the game and wait for the game to finish. """
        await self.lock.acquire()
        list = await self.requestor.list_games()
        for id, game_name in list.items():
            if name == game_name:
                raise Exception(f"game {game_name}/{id} already running")
        self.game_id = await self.requestor.create_game(umpire, name, password, maze)
        self.callback("registered", self.game_id)
        if not self.game_id:
            raise Exception(f"create game failed")
        await self.lock.acquire()
        return self.success

    async def timer(self):
        if not self.stopped:
            status = await self.requestor.status_game(self.game_id)
            if status and isinstance(status, collections.Mapping):
                if 'players' in status:
                    # check for new players
                    for player in status['players']:
                        player_name = player['player_name']
                        player_id = player['player_id']
                        if player_id not in self.players:
                            self.players[player_id] = player_name
                            self.callback('player', player_id, player_name)
                if 'status' in status:
                    if not self.stopped and status['status']['isStopped']:
                        # normal stop
                        self.stopped = True
                        self.success = status['status']['isSuccess']
                        self.callback('stopped', self.success)
                        self.lock.release()
                        return
                    if not self.started and status['status']['isStarted']:
                        # normal game start
                        self.started = True
                        self.stopped = False
                        self.callback('started')
                if 'tick' in status and status['tick'] != self.game_tick:
                    self.game_tick = status['tick']
                    self.callback('tick', self.game_tick)
                if len(status) <= 0:
                    # emergency stop
                    self.stopped = True
                    self.success = False
                    self.callback('stopped', self.success)
                    self.lock.release()
                    return

    def callback(self, cmd, *args):
        invert_op = getattr(self.client, cmd, None)
        if callable(invert_op):
            invert_op(*args)
