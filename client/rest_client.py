import os
import requests
import functools
from monitor.trace_log import TraceLog


class RestClient:

    def __init__(self, loop, url):
        self.loop = loop
        self.url = url
        self.last_player_status_tick = {}
        self.last_recording_tick = {}
        self.last_gamestatus_tick = {}
        self.last_move = {}

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

    async def delete_game(self, game_id):
        reply = await self.loop.run_in_executor(
            None, functools.partial(requests.put, self.create_url(f"game/{game_id}/stop")))
        if reply.status_code == 200:
            result = reply.json()
            return True
        else:
            raise Exception(f"failed rest call delete_game:{reply.text}")

    async def register_player(self, player_name, game_id, password):
        spec = {
            "player_name": player_name,
            "game_password": password,
        }
        reply = await self.loop.run_in_executor(
            None, functools.partial(requests.post, self.create_url(f'game/{game_id}/player'), json=spec))
        if reply.status_code == 200:
            result = reply.json()
            return result
        else:
            raise Exception(f"failed rest call register_player:{reply.text}")

    async def deregister_player(self, game_id, player_id):
        spec = {
        }
        reply = await self.loop.run_in_executor(
            None, functools.partial(requests.delete, self.create_url(f'game/{game_id}/player/{player_id}'), json=spec))
        if reply.status_code == 200:
            result = reply.json()
            return result
        else:
            raise Exception(f"failed rest call deregister_player:{reply.text}")

    async def issue_command(self, game_id, player_id, move):
        if game_id in self.last_player_status_tick:
            TraceLog.default_logger().trace('player.issue_command', self.last_player_status_tick[game_id], game_id, player_id, move)
        else:
            TraceLog.default_logger().trace('player.issue_command', -1, game_id, player_id, move)
        query = {
            'move': move
        }
        try:
            reply = await self.loop.run_in_executor(
                None, functools.partial(requests.put, self.create_url(f'game/{game_id}/player/{player_id}'), json=query))
        except Exception as e:
            pass
        if reply.status_code == 200:
            result = reply.json()
            return result
        else:
            raise Exception(f"failed rest call issue_command:{reply.text}")

    async def map_game(self, game_id):
        reply = await self.loop.run_in_executor(None, requests.get, self.create_url(f"game/{game_id}/map"))
        if reply.status_code == 200:
            result = reply.json()
            return result
        else:
            raise Exception(f"failed rest call map_game:{reply.reason}")

    async def status_game(self, game_id):
        reply = await self.loop.run_in_executor(None, requests.get, self.create_url(f"game/{game_id}/status"))
        if reply.status_code == 200:
            result = reply.json()
            game_tick = result['status']['game_tick']
            for player_id, player in result['players'].items():
                robos = player['robos']
                for robo_id, robo in robos.items():
                    if (robo_id not in self.last_gamestatus_tick) or (game_tick > self.last_gamestatus_tick[robo_id]):
                        TraceLog.default_logger().trace('umpire.gamestatus', game_tick, robo['pos'], robo['load'], robo['dir'])
                    self.last_gamestatus_tick[robo_id] = game_tick
            return result
        else:
            raise Exception(f"failed rest call status_game:{reply.reason}")

    async def status_player(self, game_id, player_id):
        reply = await self.loop.run_in_executor(None, requests.get, self.create_url(f"game/{game_id}/player/{player_id}/status"))
        if reply.status_code == 200:
            result = reply.json()
            if result:
                game_id = result['game_status']['game_id']
                game_tick = result['game_status']['status']['game_tick']
                robos = result['player_status']['robos']
                for robo_id, robo in robos.items():
                    recording = robo['recording']
                    for rec in recording:
                        if (robo_id not in self.last_recording_tick) or (rec[0] > self.last_recording_tick[robo_id]):
                            TraceLog.default_logger().trace('player.recorded_command', rec[0], game_id, player_id, [0, robo_id, rec[1]]+rec[2], rec[3])
                            self.last_recording_tick[robo_id] = rec[0]
                self.last_player_status_tick[game_id] = game_tick
            return result
        else:
            raise Exception(f"failed rest call status_player:{reply.reason}")

    def create_url(self, part):
        full = os.path.join(self.url, part)
        return full

