import unittest

class FirstTests(unittest.TestCase):

    def test_first(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()