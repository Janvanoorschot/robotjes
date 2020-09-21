import requests
from . import CLIRequestor

class CLIUmpire():

    def __init__(self, loop, url):
        self.requestor = CLIRequestor(loop, url)

    async def run_game(self, umpire, name, password, maze):
        game_id = await self.requestor.create_game(umpire, name, password, maze)
        status = await self.requestor.status_game(game_id)
        return status
