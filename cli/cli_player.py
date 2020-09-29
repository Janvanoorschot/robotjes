import collections
import asyncio
import importlib
import uuid

from . import CLIRequestor


class CLIPlayer():
    """
    https://docs.python.org/3/library/importlib.html#importlib.import_module
    """

    def __init__(self, loop, url):
        self.requestor = CLIRequestor(loop, url)
        self.player_id = str(uuid.uuid4())
        self.game_id = None
        self.ready = False
        self.success = False
        self.started = False
        self.stopped = False
        self.lock = asyncio.Lock()

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
                if success:
                    # the game has not yet started, that should come later
                    pass
                else:
                    raise Exception(f"can not join game {game_name}")
        await self.lock.acquire()
        return self.success

    async def timer(self):
        if not self.ready:
            status = await self.requestor.status_game(self.game_id)
            if self.started and isinstance(status, collections.Mapping) and len(status) <= 0:
                self.lock.release()
                return
            if not self.started and isinstance(status, collections.Mapping) and len(status) > 0 and status['status']['isStarted']:
                self.started = True
            if not self.stopped and status['status']['isStopped']:
                self.stopped = True
                self.succes = status['status']['isSuccess']
                self.lock.release()
                return
