import unittest
import os

from test import go_robo

TESTDIR = os.path.dirname(os.path.abspath(__file__))
ROOTDIR = os.path.abspath(os.path.join(TESTDIR, os.pardir))


class Sim4TestCase(unittest.TestCase):
    """ Test Scripts and Robo logic """


    def test_sim401(self):
        """reproduce the bug where the 'quit()' command is not supported"""
        map_file = os.path.join(TESTDIR, 'datafiles', 'sim4.map')
        script_file = os.path.join(TESTDIR, 'datafiles', 'sim401.py')
        success_file = os.path.join(TESTDIR, 'datafiles', 'sim4.json')
        [engine, recording, success] = go_robo(map_file, script_file, success_file)
        self.assertTrue(recording.isSuccess() and success.isSuccess())

    def test_sim402(self):
        """reproduce the bug where the 'stopPainting()' goes out of control"""
        map_file = os.path.join(TESTDIR, 'datafiles', 'sim4.map')
        script_file = os.path.join(TESTDIR, 'datafiles', 'sim402.py')
        success_file = os.path.join(TESTDIR, 'datafiles', 'sim4.json')
        [engine, recording, success] = go_robo(map_file, script_file, success_file)
        self.assertTrue(recording.isSuccess() and success.isSuccess())

if __name__ == '__main__':
    unittest.main()
