import unittest
import os

from test import go_robo

TESTDIR = os.path.dirname(os.path.abspath(__file__))
ROOTDIR = os.path.abspath(os.path.join(TESTDIR, os.pardir))


class Sim3TestCase(unittest.TestCase):
    """ Test Scripts and Robo logic """

    def test_sim301(self):
        map_file = os.path.join(TESTDIR, 'datafiles', 'sim3.map')
        script_file = os.path.join(TESTDIR, 'datafiles', 'sim301.py')
        success_file = os.path.join(TESTDIR, 'datafiles', 'sim3.json')
        [engine, recording, success] = go_robo(map_file, script_file, success_file)
        self.assertTrue(recording.isSuccess() and success.isSuccess())

    def test_sim302(self):
        map_file = os.path.join(TESTDIR, 'datafiles', 'sim3.map')
        script_file = os.path.join(TESTDIR, 'datafiles', 'sim302.py')
        success_file = os.path.join(TESTDIR, 'datafiles', 'sim3.json')
        [engine, recording, success] = go_robo(map_file, script_file, success_file)
        self.assertTrue(not recording.isSuccess() and success.isSuccess())

    def test_sim303(self):
        map_file = os.path.join(TESTDIR, 'datafiles', 'sim3.map')
        script_file = os.path.join(TESTDIR, 'datafiles', 'sim303.py')
        success_file = os.path.join(TESTDIR, 'datafiles', 'sim3.json')
        [engine, recording, success] = go_robo(map_file, script_file, success_file)
        self.assertTrue(not recording.isSuccess() and success.isSuccess())

    def test_sim304(self):
        map_file = os.path.join(TESTDIR, 'datafiles', 'sim3.map')
        script_file = os.path.join(TESTDIR, 'datafiles', 'sim304.py')
        success_file = os.path.join(TESTDIR, 'datafiles', 'sim3.json')
        [engine, recording, success] = go_robo(map_file, script_file, success_file)
        self.assertTrue(not recording.isSuccess() and success.isSuccess())


if __name__ == '__main__':
    unittest.main()
