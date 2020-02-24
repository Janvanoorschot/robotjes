import os
import unittest
from robotjes.sim import map, maze

DIR = os.path.dirname(os.path.abspath(__file__))

class MazeTestCase(unittest.TestCase):

    def test_maze101(self):
        data_file = os.path.join(DIR, os.pardir, 'datafiles/challenges/findBeacon1/findBeacon1.map')
        mz = maze.Maze(data_file)
        self.assertTrue(mz is not None)


if __name__ == '__main__':
    unittest.main()
