import unittest
from robotjes.sim.success import ROBO_SEMANTICS, ROBO_LANGUAGE


class LanguageTestCase(unittest.TestCase):
    """ Test Language features."""

    PROGRAMS = [
        "black(10,12) and black(14,12) and black(10,16) and black(14,16)",
        "white(10,12) or white(14,12) or white(10,16) or white(14,16)",
        "not maxEats(0)",
        "robot(37,16) and beacon(12,2,2) and beacon(19,2,2) and beacon(27,2,2) and beacon(34,2,2) and not robotHasBeacon",
        "not beacon(12,2,2) or not beacon(19,2,2) or not beacon(27,2,2) or not beacon(34,2,2)",
    ]


    def test_language101(self):

        lang = ROBO_LANGUAGE
        sem = ROBO_SEMANTICS
        world = None

        for line in self.PROGRAMS:
            parseResult = lang.parseString(line)
            expr = parseResult[0]
            result = expr.eval(world, sem)
            self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()