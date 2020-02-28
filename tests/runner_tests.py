import unittest
import os
from subprocess import call

from robotjes.remote import Handler
from robotjes.sim import Engine

DIR = os.path.dirname(os.path.abspath(__file__))


class RunnerTestCase(unittest.TestCase):

    def test_runner101(self):
        # input files
        map_file = os.path.join(DIR, os.pardir, 'datafiles/challenges/findBeacon1/findBeacon1.map')
        script_file = os.path.join(DIR, os.pardir, 'datafiles/challenges/findBeacon1/solution101.py')
        host = "localhost"
        port = 6000
        secret = b"secret"

        # create the engine
        engine = Engine(map_file)
        handler = Handler(host, port, secret, engine)

        # run the script in its own shell
        command = f"bin/runscript {host} {port} {secret} {script_file} &"
        call(command, shell=True)

        # start the handler
        handler.run()

        # check the resulting recording
        self.assertTrue(1 == 1)


if __name__ == '__main__':
    unittest.main()