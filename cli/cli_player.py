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
        self.player_id = None
        self.game_id = None
        self.tick = None
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
                result = await self.requestor.register_player(player_name, self.game_id, password)
                if not result:
                    raise Exception(f"can not join game {game_name}")
                else:
                    self.player_id = result['player_id']
                    self.callback('registered', self.player_id, player_name)
                break
        else:
            raise Exception(f"no such game {game_name}")
        await self.lock.acquire()
        return self.success

    async def timer(self):
        if not self.stopped:
            status = await self.requestor.status_player(self.game_id, self.player_id)
            if status and isinstance(status, collections.Mapping):
                player_status = status['player_status']
                game_status = status['game_status']
                if not self.stopped and game_status['status']['isStopped']:
                    # normal stop
                    self.stopped = True
                    self.success = game_status['status']['isSuccess']
                    self.callback('stopped', self.success)
                    self.lock.release()
                    return
                if not self.started and game_status['status']['isStarted']:
                    # normal game start
                    self.started = True
                    self.stopped = False
                    self.callback('started')
                tick = game_status['tick']
                game_tick = game_status['status']['game_tick']
                if game_tick != self.game_tick:
                    self.game_tick = game_tick
                    self.callback('game_tick', self.game_tick)
                if tick != self.tick:
                    self.tick = tick
                    self.callback('tick', self.tick)


    def callback(self, cmd, *args):
        invert_op = getattr(self.client, cmd, None)
        if callable(invert_op):
            invert_op(*args)

