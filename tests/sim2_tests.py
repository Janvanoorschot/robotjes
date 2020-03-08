import unittest
import os
from subprocess import call

from robotjes.remote import Handler
from robotjes.sim import Engine, Map

DIR = os.path.dirname(os.path.abspath(__file__))


class Sim2TestCase(unittest.TestCase):
    """ Test the Engine."""

    def init(self, map_file):
        host = "localhost"
        port = 6000
        secret = b"secret"
        self.engine = Engine(Map.fromfile(map_file))
        self.handler = Handler(host, port, secret)
        return [self.engine]

    def exec(self, script_file):
        with open(script_file) as script:
            self.handler.run_client(script)
        self.handler.run(self.engine)
        return [self.engine]

    def test_sim201(self):
        map_file = os.path.join(DIR, os.pardir, 'tests/datafiles', 'sim2.map')
        script_file = os.path.join(DIR, os.pardir, 'tests/datafiles', 'sim201.py')
        # bot starts at (11,11)
        [engine] = self.init(map_file)
        self.assertEqual((7, 11), engine.maze.bot.pos)
        self.assertEqual(90, engine.maze.bot.dir)
        [engine] = self.exec(script_file)
        self.assertEqual(0, engine.maze.bot.dir)
        self.assertEqual((14, 11), engine.maze.bot.pos)

    def test_sim202(self):
        map_file = os.path.join(DIR, os.pardir, 'tests/datafiles', 'sim2.map')
        script_file = os.path.join(DIR, os.pardir, 'tests/datafiles', 'sim201.py')
        # bot starts at (11,11)
        [engine] = self.init(map_file)
        [engine] = self.exec(script_file)
        recording = engine.recording
        self.assertEqual(16, len(recording.keyframes))
        map = recording.toMap()
        self.assertEqual(16,len(map))


if __name__ == '__main__':
    unittest.main()