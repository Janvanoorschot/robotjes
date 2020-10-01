import collections
import asyncio
import importlib
import uuid

from . import CLIRequestor


class CLIPlayer():
    """
    https://docs.python.org/3/library/importlib.html#importlib.import_module
    """

    def __init__(self, loop, url, client):
        self.requestor = CLIRequestor(loop, url)
        self.client = client
        self.player_id = str(uuid.uuid4())
        self.game_id = None
        self.game_tick = None
        self.success = False
        self.started = False
        self.stopped = False
        self.lock = asyncio.Lock()
        self.players = {}

    async def run_game(self, player_name, game_name, password, module_name):
        """ Validate the params, join the game and wait for the game to finish. """
        await self.lock.acquire()
        list = await self.requestor.list_games()
        for id, name in list.items():
            if game_name == name:
                self.game_id = id
                module  = importlib.import_module(module_name)
                if hasattr(module, 'player'):
                    player = module.player
                else:
                    raise Exception(f"invalid player module {module_name}")
                success = await self.requestor.register_player(self.player_id, player_name, self.game_id, password)
                if not success:
                    raise Exception(f"can not join game {game_name}")
                else:
                    self.callback('registered', self.player_id)
                break
        else:
            raise Exception(f"no such game {game_name}")
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

