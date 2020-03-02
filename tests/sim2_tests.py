import unittest
import os
from subprocess import call

from robotjes.remote import Handler
from robotjes.sim import Engine

DIR = os.path.dirname(os.path.abspath(__file__))


class Sim2TestCase(unittest.TestCase):

    def init(self, map_file_name, script_file_name):
        map_file = os.path.join(DIR, os.pardir, 'tests/datafiles', map_file_name)
        script_file = os.path.join(DIR, os.pardir, 'tests/datafiles', script_file_name)
        host = "localhost"
        port = 6000
        secret = b"secret"
        self.engine = Engine(map_file)
        self.handler = Handler(host, port, secret, self.engine)
        self.command = f"bin/runscript {host} {port} {secret} {script_file} &"
        return [self.engine]

    def exec(self):
        call(self.command, shell=True)
        self.handler.run()
        return [self.engine]

    def test_sim201(self):
        # bot starts at (11,11)
        [engine] = self.init('sim2.map', 'sim201.py')
        self.assertEqual((7, 11), engine.maze.bot.pos)
        self.assertEqual(90, engine.maze.bot.dir)
        [engine] = self.exec()
        self.assertEqual(0, engine.maze.bot.dir)
        self.assertEqual((14, 11), engine.maze.bot.pos)

    def test_sim202(self):
        # bot starts at (11,11)
        [engine] = self.init('sim2.map', 'sim201.py')
        [engine] = self.exec()
        recording = engine.recording
        self.assertEqual(16, len(recording.keyframes))


if __name__ == '__main__':
    unittest.main()