import unittest
import os
from robotjes.dev import DevRequestor, DevRunner, DevHandler

DIR = os.path.dirname(os.path.abspath(__file__))


class RunnerTestCase(unittest.TestCase):

    def test_runner101(self):
        # input files
        map_file = os.path.join(DIR, os.pardir, 'datafiles/challenges/findBeacon1/findBeacon1.map')
        script_file = os.path.join(DIR, os.pardir, 'datafiles/challenges/findBeacon1/solution101.py')
        # compose the run-time environment
        runner = DevRunner(requestor, handler)

        recording = runner.run(map_file, script_file)



if __name__ == '__main__':
    unittest.main()