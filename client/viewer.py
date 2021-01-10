import asyncio
from robotjes.bot import RoboThread, Robo
import sys

import concurrent

from client import RestClient
from robotjes.local import LocalRequestor


class CLIViewer:

    def __init__(self, loop, url, client):
        self.loop = loop
        self.rest_client = RestClient(loop, url)
        self.client = client
        self.game_id = None
        self.tick = None
        self.game_tick = None
        self.before_game_time = 0
        self.lock = asyncio.Lock()

        self.running = False
        self.started = False
        self.stopped = False
        self.success = False
        self.robo_coroutine = None
        self.players = {}
        self.player_status = None
        self.game_status = None
        self.robo_status = {}
        self.client_code = None
        self.robo = None

    async def stop(self):
        sys.exit("viewer break")

    async def run_game(self, game_name, password):
        await self.lock.acquire()
        list = await self.rest_client.list_games()
        for id, name in list.items():
            if game_name == name:
                self.game_id = id
                break
        else:
            raise Exception(f"no such game {game_name}")
        await self.lock.acquire()


    async def timer(self):
        if not self.stopped:
            try:
                status = await self.rest_client.recording_game(self.game_id, self.before_game_time)
            except Exception as e:
                print(f"failed to get player status: {e}")
                return
            if status:
                # we received a valid delta-recording, handle it
                for delta in status:
                    game_tick = delta['game_tick']
                    frames = delta['frames']
                    map_status = delta['map_status']
                    self.before_game_time = game_tick

    def set_game_status(self, game_tick, game_status):
        self.callback('game_status', game_tick, game_status)
        self.game_status = game_status
        if not self.stopped and game_status['status']['isStopped']:
            # normal stop
            self.stopped = True
            self.success = game_status['status']['isSuccess']
            self.callback('stopped', self.success)
            return
        if not self.started and game_status['status']['isStarted']:
            # normal game start
            self.started = True
            self.stopped = False
            self.callback('started')
        if game_tick != self.game_tick:
            self.game_tick = game_tick
            if self.timer_lock.locked():
                self.timer_lock.release()

    def set_player_status(self, game_tick, player_status):
        self.callback('player_status', game_tick, player_status)

    def set_robo_status(self, game_tick, robo_id, robo_status):
        self.callback('robo_status', game_tick, robo_id, robo_status)
        if robo_id not in self.robo_status:
            # first time we see this robo, activate its logic
            self.robo.set_id(robo_id)
            self.robo_coroutine = self.loop.run_in_executor(
               self.executor,
               self.client_code.run)
        self.robo_status[robo_id] = robo_status

    def callback(self, cmd, *args):
        invert_op = getattr(self.client, cmd, None)
        if callable(invert_op):
            invert_op(*args)

