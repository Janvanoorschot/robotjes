import unittest
import os
from subprocess import call

from robotjes.remote import Handler
from robotjes.sim import Engine

DIR = os.path.dirname(os.path.abspath(__file__))


class SimTestCase(unittest.TestCase):

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

    def test_sim101(self):
        # bot starts at (11,11)
        [engine] = self.init('sim1.map', 'sim101.py')
        self.assertEqual((11, 11), engine.maze.bot.pos)
        self.assertEqual(90, engine.maze.bot.dir)
        [engine] = self.exec()
        self.assertEqual((10, 11), engine.maze.bot.pos)
        self.assertEqual(180, engine.maze.bot.dir)

    def test_sim102(self):
        # bot starts at (11,11)
        [engine] = self.init('sim1.map', 'sim102.py')
        [engine] = self.exec()
        self.assertEqual((11, 11), engine.maze.bot.pos)
        self.assertEqual(90, engine.maze.bot.dir)

    def test_sim103(self):
        # bot starts at (11,11)
        [engine] = self.init('sim1.map', 'sim103.py')
        self.assertEqual(0, len(engine.maze.bot.beacons))
        [engine] = self.exec()
        self.assertEqual((10, 12), engine.maze.bot.pos)
        self.assertEqual(90, engine.maze.bot.dir)
        self.assertEqual(1, len(engine.maze.bot.beacons))


if __name__ == '__main__':
    unittest.main()