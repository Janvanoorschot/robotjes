import unittest
import os
from subprocess import call

from robotjes.remote import Handler
from robotjes.sim import Engine

DIR = os.path.dirname(os.path.abspath(__file__))


class SimTestCase(unittest.TestCase):

    def exec(self, map_file_name, script_file_name):
        map_file = os.path.join(DIR, os.pardir, 'tests/datafiles', map_file_name)
        script_file = os.path.join(DIR, os.pardir, 'tests/datafiles', script_file_name)
        host = "localhost"
        port = 6000
        secret = b"secret"
        engine = Engine(map_file)
        handler = Handler(host, port, secret, engine)
        command = f"bin/runscript {host} {port} {secret} {script_file} &"
        call(command, shell=True)
        handler.run()
        return [engine]

    def test_runner101(self):
        [engine] = self.exec('sim101.map', 'sim101.py')
        self.assertEqual((11, 10), engine.maze.bot.pos)


if __name__ == '__main__':
    unittest.main()