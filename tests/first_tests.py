import unittest
import os
from robotjes.map import mapper

DIR = os.path.dirname(os.path.abspath(__file__))

class FirstTests(unittest.TestCase):

    def test_first(self):
        data_file = os.path.join(DIR, os.pardir, 'datafiles/challenges/findBeacon1/findBeacon1.map')
        map = mapper.Mapper.fromfile(data_file)
        self.assertTrue( not map is None)

if __name__ == '__main__':
    unittest.main()