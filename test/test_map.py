import unittest
import os
from robotjessrv.sim import map

DIR = os.path.dirname(os.path.abspath(__file__))


class MapTestCase(unittest.TestCase):

    def test_map101(self):
        data_file = os.path.join(DIR, os.pardir, 'datafiles/challenges/findBeacon1/findBeacon1.map')
        m = map.Map.fromfile(data_file)
        self.assertTrue(m is not None)

    def test_map102(self):
        data_file = os.path.join(DIR, os.pardir, 'datafiles/challenges/introFlipCoin/default.map')
        m = map.Map.fromfile(data_file)
        self.assertTrue(m is not None)


if __name__ == '__main__':
    unittest.main()