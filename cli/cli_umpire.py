import collections
from . import CLIRequestor
import asyncio


class CLIUmpire():

    def __init__(self, loop, url):
        self.requestor = CLIRequestor(loop, url)
        self.game_id = None
        self.ready = False
        self.success = False
        self.started = False
        self.lock = asyncio.Lock()

    async def run_game(self, umpire, name, password, maze):
        """ Validate the params, create the game and wait for the game to finish. """
        await self.lock.acquire()
        list = await self.requestor.list_games()
        for id, game_name in list.items():
            if name == game_name:
                raise Exception(f"game {game_name}/{id} already running")
        self.game_id = await self.requestor.create_game(umpire, name, password, maze)
        if not self.game_id:
            raise Exception(f"create game failed")
        await self.lock.acquire()
        return self.game_id

    async def timer(self):
        if not self.ready:
            status = await self.requestor.status_game(self.game_id)
            if isinstance(status, collections.Mapping) and len(status) > 0:
                self.started = True
            if self.started:
                isStarted = status['status']['isStarted']
                isStopped = status['status']['isStopped']
                isSuccess = status['status']['isSuccess']
                print(f"{isStarted}/{isStopped}/{isSuccess}")
                # self.lock.release()
