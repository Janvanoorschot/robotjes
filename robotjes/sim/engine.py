from .maze import Maze
from .map import Map
from .recording import Recording

LEGAL_COMMANDS = ["forward", "backward", "left", "right", "pickUp", "putDown",
                  "eatUp", "paintWhite", "paintBlack", "stopPainting",
                  "leftIsClear", "leftIsObstacle", "leftIsBeacon", "leftIsWhite", "leftIsBlack",
                  "frontIsClear", "frontIsObstacle", "frontIsBeacon", "frontIsWhite", "frontIsBlack",
                  "rightIsClear", "rightIsObstacle", "rightIsBeacon", "rightIsWhite", "rightIsBlack",
                  "flipCoin", "message"
                  ]
class Engine(object):

    def __init__(self, map):
        self.map = map
        self.maze = Maze(self.map)
        self.recording = Recording()

    def get_recording(self):
        return self.recording

    def clean_cmd(self, cmd):
        if not cmd or not type(cmd)==list or len(cmd)< 2:
            return ["illegal"]
        [id, command, *args] = cmd
        if command not in LEGAL_COMMANDS:
            return ["unknown"]
        else:
            return [command, *args]

    def prepare_reply(self, cmd, *args):
        reply = [cmd, args]
        return reply

    def execute(self, cmd):
        [command, *args] = self.clean_cmd(cmd)
        reply = []
        if command == "forward":
            expected = 1 if len(args) < 1 else args[0]
            actual = 0
            for i in range(expected):
                next_pos = self.maze.calc_pos(self.maze.bot, self.maze.FRONT, +1)
                if next_pos and self.maze.available_pos(next_pos):
                    success = self.maze.move_to(next_pos)
                    reply.append([success, next_pos])
                    actual = actual + 1
                else:
                    self.recording.boom(cmd)
                    reply.append([False, next_pos])
            self.recording.forward(actual, expected)
        elif command == "backward":
            expected = 1 if len(args) < 1 else args[0]
            actual = 0
            for i in range(expected):
                next_pos = self.maze.calc_pos(self.maze.bot, self.maze.FRONT, -1)
                if next_pos and self.maze.available_pos(next_pos):
                    success = self.maze.move_to(next_pos)
                    reply.append([success, next_pos])
                    actual = actual + 1
                else:
                    self.recording.boom(cmd)
                    reply.append([False, next_pos])
            self.recording.backward(actual, expected)
        elif command == "right":
            expected = 1 if len(args) < 1 else args[0]
            for i in range(expected):
                dir = self.maze.right()
                reply.append([True, dir])
            self.recording.right(expected)
        elif command == "left":
            expected = 1 if len(args) < 1 else args[0]
            for i in range(expected):
                dir = self.maze.left()
                reply.append([True, dir])
            self.recording.left(expected)
        elif command == "pickUp":
            success = self.maze.pickUp()
            reply.append([success])
            self.recording.pickUp(success)
        elif command == "putDown":
            success = self.maze.putDown()
            reply.append([success])
            self.recording.putDown(success)
        elif command == "eatUp":
            success = self.maze.eatUp()
            reply.append([success])
            self.recording.eatUp(success)
        elif command == "paintWhite":
            start = self.maze.paintWhite()
            reply.append([start])
            self.recording.paintWhite(start)
        elif command == "paintBlack":
            start = self.maze.paintBlack()
            reply.append([start])
            self.recording.paintBlack(start)
        elif command == "stopPainting":
            start = self.maze.stopPainting()
            reply.append([start])
            self.recording.stopPainting(start)
        elif command == "leftIsClear":
            success = self.maze.check(Maze.LEFT, Maze.CLEAR)
            self.recording.see("left", "clear")
            reply.append([success])
        elif command == "leftIsObstacle":
            success = self.maze.check(Maze.LEFT, Maze.OBSTACLE)
            self.recording.see("left", "obstacle")
            reply.append([success])
        elif command == "leftisBeacon":
            success = self.maze.check(Maze.LEFT, Maze.BEACON)
            self.recording.see("left", "beacon")
            reply.append([success])
        elif command == "leftIsWhite":
            success = self.maze.check(Maze.LEFT, Maze.WHITE)
            self.recording.see("left", "white")
            reply.append([success])
        elif command == "leftIsBlack":
            success = self.maze.check(Maze.LEFT, Maze.BLACK)
            self.recording.see("left", "black")
            reply.append([success])
        elif command == "frontIsClear":
            success = self.maze.check(Maze.FRONT, Maze.CLEAR)
            self.recording.see("front", "clear")
            reply.append([success])
        elif command == "frontIsObstacle":
            success = self.maze.check(Maze.FRONT, Maze.OBSTACLE)
            self.recording.see("front", "obstacle")
            reply.append([success])
        elif command == "frontisBeacon":
            success = self.maze.check(Maze.FRONT, Maze.BEACON)
            self.recording.see("front", "beacon")
            reply.append([success])
        elif command == "frontIsWhite":
            success = self.maze.check(Maze.FRONT, Maze.WHITE)
            self.recording.see("front", "white")
            reply.append([success])
        elif command == "frontIsBlack":
            success = self.maze.check(Maze.FRONT, Maze.BLACK)
            self.recording.see("front", "black")
            reply.append([success])
        elif command == "rightIsClear":
            success = self.maze.check(Maze.RIGHT, Maze.CLEAR)
            self.recording.see("right", "clear")
            reply.append([success])
        elif command == "rightIsObstacle":
            success = self.maze.check(Maze.RIGHT, Maze.OBSTACLE)
            self.recording.see("right", "obstacle")
            reply.append([success])
        elif command == "rightisBeacon":
            success = self.maze.check(Maze.RIGHT, Maze.BEACON)
            self.recording.see("right", "beacon")
            reply.append([success])
        elif command == "rightIsWhite":
            success = self.maze.check(Maze.RIGHT, Maze.WHITE)
            self.recording.see("right", "white")
            reply.append([success])
        elif command == "rightIsBlack":
            success = self.maze.check(Maze.RIGHT, Maze.BLACK)
            self.recording.see("right", "black")
            reply.append([success])
        elif command == "flipCoin":
            result = self.maze.flipCoin()
            self.recording.flipCoin()
            reply.append([result])
        elif command == "message":
            message = "unknown" if len(args) < 1 else args[0]
            self.recording.message(message)
        else:
            reply.append([False])
        return self.prepare_reply(cmd, reply)

