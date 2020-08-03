from .world import World
from .recording import Recording

LEGAL_COMMANDS = ["forward", "backward", "left", "right", "pickUp", "putDown",
                  "eatUp", "paintWhite", "paintBlack", "stopPainting",
                  "leftIsClear", "leftIsObstacle", "leftIsBeacon", "leftIsWhite", "leftIsBlack",
                  "frontIsClear", "frontIsObstacle", "frontIsBeacon", "frontIsWhite", "frontIsBlack",
                  "rightIsClear", "rightIsObstacle", "rightIsBeacon", "rightIsWhite", "rightIsBlack",
                  "flipCoin", "message", "stdout", "stderr"
                  ]
class Engine(object):

    def __init__(self, map):
        self.map = map
        self.world = World(self.map)
        self.recording = Recording()

    def get_recording(self):
        return self.recording

    def get_profile(self):
        return self.world.profile

    def clean_cmd(self, cmd):
        if not cmd or not type(cmd)==list or len(cmd)< 3:
            return ["illegal"]
        [lineno, id, command, *args] = cmd
        if command not in LEGAL_COMMANDS:
            return ["unknown", 0, []]
        else:
            return [command, lineno, *args]

    def prepare_reply(self, cmd, *args):
        reply = [cmd, args]
        return reply

    def execute(self, cmd):
        [command, lineno, *args] = self.clean_cmd(cmd)
        reply = []
        self.world.inc("scriptCalls")
        self.world.inc("scriptBasicCommands")
        self.recording.lineno(lineno)
        if command == "forward":
            expected = 1 if len(args) < 1 else int(args[0])
            actual = 0
            for i in range(expected):
                next_pos = self.world.calc_pos(self.world.bot, self.world.FRONT, +1)
                if next_pos and self.world.available_pos(next_pos):
                    success = self.world.move_to(next_pos)
                    reply.append([success, next_pos])
                    actual = actual + 1
                else:
                    self.recording.boom(cmd)
                    reply.append([False, next_pos])
                    self.world.inc("robotHasBumped")
            self.recording.forward(actual, expected)
        elif command == "backward":
            expected = 1 if len(args) < 1 else int(args[0])
            actual = 0
            for i in range(expected):
                next_pos = self.world.calc_pos(self.world.bot, self.world.FRONT, -1)
                if next_pos and self.world.available_pos(next_pos):
                    success = self.world.move_to(next_pos)
                    reply.append([success, next_pos])
                    actual = actual + 1
                else:
                    self.recording.boom(cmd)
                    reply.append([False, next_pos])
                    self.world.inc("robotHasBumped")
            self.recording.backward(actual, expected)
        elif command == "right":
            expected = 1 if len(args) < 1 else int(args[0])
            for i in range(expected):
                dir = self.world.right()
                reply.append([True, dir])
            self.recording.right(expected)
        elif command == "left":
            expected = 1 if len(args) < 1 else int(args[0])
            for i in range(expected):
                dir = self.world.left()
                reply.append([True, dir])
            self.recording.left(expected)
        elif command == "pickUp":
            success = self.world.pickUp()
            reply.append([success])
            self.recording.pickUp(success)
        elif command == "putDown":
            success = self.world.putDown()
            reply.append([success])
            self.recording.putDown(success)
        elif command == "eatUp":
            success = self.world.eatUp()
            reply.append([success])
            self.recording.eatUp(success)
        elif command == "paintWhite":
            start = self.world.paintWhite()
            reply.append([start])
            self.recording.paintWhite(start)
        elif command == "paintBlack":
            start = self.world.paintBlack()
            reply.append([start])
            self.recording.paintBlack(start)
        elif command == "stopPainting":
            start = self.world.stopPainting()
            reply.append([start])
            self.recording.stopPainting()
        elif command == "leftIsClear":
            success = self.world.check(World.LEFT, World.CLEAR)
            self.recording.see("left", "clear")
            reply.append([success])
            self.world.inc("see")
        elif command == "leftIsObstacle":
            success = self.world.check(World.LEFT, World.OBSTACLE)
            self.recording.see("left", "obstacle")
            reply.append([success])
            self.world.inc("see")
        elif command == "leftIsBeacon":
            success = self.world.check(World.LEFT, World.BEACON)
            self.recording.see("left", "beacon")
            reply.append([success])
            self.world.inc("see")
        elif command == "leftIsWhite":
            success = self.world.check(World.LEFT, World.WHITE)
            self.recording.see("left", "white")
            reply.append([success])
            self.world.inc("see")
        elif command == "leftIsBlack":
            success = self.world.check(World.LEFT, World.BLACK)
            self.recording.see("left", "black")
            reply.append([success])
            self.world.inc("see")
        elif command == "frontIsClear":
            success = self.world.check(World.FRONT, World.CLEAR)
            self.recording.see("front", "clear")
            reply.append([success])
            self.world.inc("see")
        elif command == "frontIsObstacle":
            success = self.world.check(World.FRONT, World.OBSTACLE)
            self.recording.see("front", "obstacle")
            reply.append([success])
            self.world.inc("see")
        elif command == "frontIsBeacon":
            success = self.world.check(World.FRONT, World.BEACON)
            self.recording.see("front", "beacon")
            reply.append([success])
            self.world.inc("see")
        elif command == "frontIsWhite":
            success = self.world.check(World.FRONT, World.WHITE)
            self.recording.see("front", "white")
            reply.append([success])
            self.world.inc("see")
        elif command == "frontIsBlack":
            success = self.world.check(World.FRONT, World.BLACK)
            self.recording.see("front", "black")
            reply.append([success])
            self.world.inc("see")
        elif command == "rightIsClear":
            success = self.world.check(World.RIGHT, World.CLEAR)
            self.recording.see("right", "clear")
            reply.append([success])
            self.world.inc("see")
        elif command == "rightIsObstacle":
            success = self.world.check(World.RIGHT, World.OBSTACLE)
            self.recording.see("right", "obstacle")
            reply.append([success])
            self.world.inc("see")
        elif command == "rightIsBeacon":
            success = self.world.check(World.RIGHT, World.BEACON)
            self.recording.see("right", "beacon")
            reply.append([success])
            self.world.inc("see")
        elif command == "rightIsWhite":
            success = self.world.check(World.RIGHT, World.WHITE)
            self.recording.see("right", "white")
            reply.append([success])
            self.world.inc("see")
        elif command == "rightIsBlack":
            success = self.world.check(World.RIGHT, World.BLACK)
            self.recording.see("right", "black")
            reply.append([success])
            self.world.inc("see")
        elif command == "flipCoin":
            result = self.world.flipCoin()
            self.recording.flipCoin()
            reply.append([result])
            self.world.inc("flipCoins")
        elif command == "message":
            message = "unknown" if len(args) < 1 else args[0]
            loc = self.world.getLoc()
            cargo = self.world.getCargo()
            paint = self.world.getPaint()
            message = message.format(loc=loc, cargo=cargo, paint=paint)
            self.recording.message(message)
        elif command == "stderr":
            message = "none" if len(args) < 1 else args[0]
            if len(message)>1 and message != "none":
                pass
        elif command == "stdout":
            message = "none" if len(args) < 1 else args[0]
            if len(message)>1 and message != "none":
                pass
        else:
            reply.append([False])
        return self.prepare_reply(cmd, reply)

