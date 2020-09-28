import os
import requests
import functools


class CLIRequestor:

    def __init__(self, loop, url):
        self.loop = loop
        self.url = url

    async def list_games(self):
        reply = await self.loop.run_in_executor(None, requests.get, self.create_url('games'))
        if reply.status_code == 200:
            result = reply.json()
            return result
        else:
            raise Exception(f"failed rest call list_games:{reply.reason}")

    async def create_game(self, umpire, name, password, maze):
        spec = {
            "umpire_id": umpire,
            "game_name": name,
            "game_password": password,
            "maze_id": maze
        }
        reply = await self.loop.run_in_executor(
            None, functools.partial(requests.post, self.create_url('games'), json=spec))
        if reply.status_code == 200:
            result = reply.json()
            if result['success']:
                return result['game_id']
            else:
                return None
        else:
            raise Exception(f"failed rest call create_game:{reply.text}")

    async def register_player(self, player_id, player_name, game_id, password):
        spec = {
            "player_name": player_name,
            "player_id": player_id,
            "game_password": password,
        }
        reply = await self.loop.run_in_executor(
            None, functools.partial(requests.put, self.create_url(f'game/{game_id}/register'), json=spec))
        if reply.status_code == 200:
            return True
        else:
            raise Exception(f"failed rest call register_player:{reply.text}")

    async def status_game(self, game_id):
        reply = await self.loop.run_in_executor(None, requests.get, self.create_url(f"games/{game_id}"))
        if reply.status_code == 200:
            result = reply.json()
            return result
        else:
            raise Exception(f"failed rest call list_games:{reply.reason}")

    def create_url(self, part):
        full = os.path.join(self.url, part)
        return full

