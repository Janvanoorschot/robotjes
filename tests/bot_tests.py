import unittest
from robotjes.bot import robo

class BotTestCase(unittest.TestCase):

    def test_bot101(self):
        bot = robo.Robo(None)
        script = ("robo.forward(5)\n"
                  "robo.right(2)\n")
        exec(script, {}, {"robo": bot})


if __name__ == '__main__':
    unittest.main()
