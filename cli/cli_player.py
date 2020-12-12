import collections
import asyncio
import importlib
import functools
from robotjes.bot import RoboThread, Robo
import uuid

from cli import RestClient
from robotjes.local import LocalRequestor


class CLIPlayer():
    """
    https://docs.python.org/3/library/importlib.html#importlib.import_module
    """

    def __init__(self, loop, url, client):
        self.loop = loop
        self.rest_client = RestClient(loop, url)
        self.local_requestor = LocalRequestor(self.loop)
        self.client = client
        self.player_id = None
        self.game_id = None
        self.tick = None
        self.game_tick = None
        self.running = False
        self.started = False
        self.stopped = False
        self.success = False
        self.timer_lock = asyncio.Lock()
        self.robo_coroutine = None
        self.players = {}
        self.player_status = None
        self.game_status = None
        self.robo_status = {}
        self.client_code = None
        self.robo = None


    async def run_game(self, player_name, game_name, password, execute):
        """ Validate the params and  join the game. """
        list = await self.rest_client.list_games()
        for id, name in list.items():
            if game_name == name:
                self.game_id = id
                result = await self.rest_client.register_player(player_name, self.game_id, password)
                if not result:
                    raise Exception(f"can not join game {game_name}")
                else:
                    self.player_id = result['player_id']
                    self.callback('registered', self.player_id, player_name)
                break
        else:
            raise Exception(f"no such game {game_name}")

        # start the client code
        self.robo = Robo(self.local_requestor)
        self.client_code = RoboThread(self.robo, execute)
        # enter the command/reply cycle until the local_requestor is stopped
        while not self.stopped:
            cmd = await self.local_requestor.get()
            if len(cmd) < 2:
                break
            elif Robo.is_observation(cmd):
                robo_id = self.robo.id
                if robo_id in self.robo_status and 'fog_of_war' in self.robo_status[robo_id]:
                    status = self.robo_status[robo_id]
                    boolean = Robo.observation(status['fog_of_war']['fog_of_war'], cmd)
                else:
                    boolean = False
                reply = {'result': boolean}
            else:
                # at this point, we need to contact the server
                await self.rest_client.issue_command(self.game_id, self.player_id, cmd)
                reply = {'result': True}
            await self.timer_lock.acquire()
            await self.local_requestor.put(reply)
        await self.rest_client.deregister_player(self.game_id, self.player_id)
        self.robo_coroutine.cancel()
        return self.success

    async def timer(self):
        if not self.stopped:
            try:
                status = await self.rest_client.status_player(self.game_id, self.player_id)
            except Exception as e:
                print(f"failed to get player status: {e}")
                return
            if status and isinstance(status, collections.Mapping):
                # we received a valid status (about the game, this player and all the robo's), handle it
                self.set_game_status(status['game_status'])
                self.set_player_status(status['player_status'])

    def set_game_status(self, game_status):
        self.game_status = game_status
        if not self.stopped and game_status['status']['isStopped']:
            # normal stop
            self.stopped = True
            self.success = game_status['status']['isSuccess']
            self.callback('stopped', self.success)
            # await self.local_requestor.stop()
            return
        if not self.started and game_status['status']['isStarted']:
            # normal game start
            self.started = True
            self.stopped = False
            self.callback('started')
        tick = self.game_status['tick']
        game_tick = game_status['status']['game_tick']
        if game_tick != self.game_tick:
            self.game_tick = game_tick
            self.callback('game_tick', self.game_tick)
            if self.timer_lock.locked():
                self.timer_lock.release()
        if tick != self.tick:
            self.tick = tick
            self.callback('tick', self.tick)

    def set_player_status(self, player_status):
        for robo_id, fog_of_war in status['player_status']['fog_of_war'].items():
            self.set_robo_status(robo_id, fog_of_war)
        self.player_status = player_status

    def set_robo_status(self, robo_id, robo_status):
        if robo_id not in self.robo_status:
            # first time we see this robo, activate its logic
            self.robo.set_id(robo_id)
            self.robo_coroutine = self.loop.run_in_executor(
               None,
               self.client_code.run)
        self.robo_status[robo_id] = robo_status

    def callback(self, cmd, *args):
        invert_op = getattr(self.client, cmd, None)
        if callable(invert_op):
            invert_op(*args)

