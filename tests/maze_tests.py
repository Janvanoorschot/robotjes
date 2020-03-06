import os
import unittest
from robotjes.sim import map, maze

DIR = os.path.dirname(os.path.abspath(__file__))

class MazeTestCase(unittest.TestCase):

    def test_maze101(self):
        data_file = os.path.join(DIR, os.pardir, 'datafiles/challenges/findBeacon1/findBeacon1.map')
        mz = maze.Maze(map.Map.fromfile(data_file))
        self.assertTrue(mz is not None)

    def test_direction_1(self):
        self.assertEqual(maze.dir_left(90), 180)
        self.assertEqual(maze.dir_left(270), 0)
        self.assertEqual(maze.dir_left(0), 90)
        self.assertEqual(maze.dir_right(0), 270)
        self.assertEqual(maze.dir_right(90), 0)

if __name__ == '__main__':
    unittest.main()
