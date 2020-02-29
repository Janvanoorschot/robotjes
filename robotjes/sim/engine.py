from .maze import Maze
from .recording import Recording

LEGAL_COMMANDS = ["forward", "backward", "left", "right", "pickUp", "putDown",
                  "eatUp", "paintWhite", "paintBlack", "stopPainting",
                  "leftIsClear", "leftIsBeacon", "leftIsWhite", "leftIsBlack",
                  "frontIsClear", "frontIsBeacon", "frontIsWhite", "frontIsBlack",
                  "rightIsClear", "rightIsBeacon", "rightIsWhite", "rightIsBlack",
                  "flipCoin"
                  ]
class Engine(object):

    def __init__(self, map_file):
        self.map_file = map_file
        self.maze = Maze(self.map_file)
        self.recording = Recording()

    def get_recording(self):
        return None

    def clean_cmd(self, cmd):
        if not cmd or not type(cmd)==list or len(cmd)< 2:
            return ["illegal"]
        [id, command, *args] = cmd
        if command not in LEGAL_COMMANDS:
            return ["unknown"]
        else:
            return [command, *args]

    def prepare_reply(self, cmd, *args):
        print(f"!!!!!{cmd}")
        return [cmd]

    def execute(self, cmd):
        [command, *args] = self.clean_cmd(cmd)
        reply = []
        if command == "forward":
            steps = 1 if len(args) < 1 else args[0]
            for i in range(steps):
                next_pos = self.maze.calc_pos(self.maze.bot.pos, self.maze.bot.dir, +1)
                if next_pos and self.maze.available_pos(next_pos):
                    success = self.maze.move_to(next_pos)
                    self.recording.move_to(cmd, success, next_pos)
                    reply.append([success, next_pos])
                else:
                    self.recording.boom(cmd)
                    reply.append([False, next_pos])
        elif command == "backward":
            steps = 1 if len(args) < 1 else args[0]
            for i in range(steps):
                next_pos = self.maze.calc_pos(self.maze.bot.pos, self.maze.bot.dir, -1)
                if next_pos and self.maze.available_pos(next_pos):
                    success = self.maze.move_to(next_pos)
                    self.recording.move_to(cmd, success, next_pos)
                    reply.append([success, next_pos])
                else:
                    self.recording.boom(cmd)
                    reply.append([False, next_pos])
        elif command == "right":
            steps = 1 if len(args) < 1 else args[0]
            for i in range(steps):
                dir = self.maze.right()
                self.recording.right(cmd, dir)
                reply.append([True, dir])
        elif command == "left":
            steps = 1 if len(args) < 1 else args[0]
            for i in range(steps):
                dir = self.maze.left()
                self.recording.left(cmd, dir)
                reply.append([True, dir])
        elif command == "pickUp":
            success = self.maze.pickUp()
            self.recording.pickUp(cmd, success)
            reply.append([success])
        elif command == "putDown":
            success = self.maze.putDown()
            self.recording.putDown(cmd, success)
            reply.append([True])
        elif command == "eatUp":
            success = self.maze.eatUp()
            self.recording.eatUp(cmd, success)
            reply.append([True])
        elif command == "paintWhite":
            success = self.maze.paintWhite()
            self.recording.paintWhite(cmd, success)
            reply.append([success])
        elif command == "paintBlack":
            success = self.maze.paintBlack()
            self.recording.paintBlack(cmd, success)
            reply.append([success])
        elif command == "stopPainting":
            success = self.maze.stopPainting()
            self.recording.stopPainting(cmd, success)
            reply.append([success])
        elif command == "leftIsClear":
            success = self.maze.check(Maze.LEFT, Maze.CLEAR)
            self.recording.see(cmd, success)
            reply.append([success])
        elif command == "leftisBeacon":
            success = self.maze.check(Maze.LEFT, Maze.BEACON)
            self.recording.see(cmd, success)
            reply.append([success])
        elif command == "leftIsWhite":
            success = self.maze.check(Maze.LEFT, Maze.WHITE)
            self.recording.see(cmd, success)
            reply.append([success])
        elif command == "leftIsBlack":
            success = self.maze.check(Maze.LEFT, Maze.BLACK)
            self.recording.see(cmd, success)
            reply.append([success])
        elif command == "frontIsClear":
            success = self.maze.check(Maze.FRONT, Maze.CLEAR)
            self.recording.see(cmd, success)
            reply.append([success])
        elif command == "frontisBeacon":
            success = self.maze.check(Maze.FRONT, Maze.BEACON)
            self.recording.see(cmd, success)
            reply.append([success])
        elif command == "frontIsWhite":
            success = self.maze.check(Maze.FRONT, Maze.WHITE)
            self.recording.see(cmd, success)
            reply.append([success])
        elif command == "frontIsBlack":
            success = self.maze.check(Maze.FRONT, Maze.BLACK)
            self.recording.see(cmd, success)
            reply.append([success])
        elif command == "rightIsClear":
            success = self.maze.check(Maze.RIGHT, Maze.CLEAR)
            self.recording.see(cmd, success)
            reply.append([success])
        elif command == "rightisBeacon":
            success = self.maze.check(Maze.RIGHT, Maze.BEACON)
            self.recording.see(cmd, success)
            reply.append([success])
        elif command == "rightIsWhite":
            success = self.maze.check(Maze.RIGHT, Maze.WHITE)
            self.recording.see(cmd, success)
            reply.append([success])
        elif command == "rightIsBlack":
            success = self.maze.check(Maze.RIGHT, Maze.BLACK)
            self.recording.see(cmd, success)
            reply.append([success])
        elif command == "flipCoin":
            result = self.maze.flipCoin()
            self.recording.flipCoin(cmd, result)
            reply.append([result])
        else:
            reply.append([False])
        return self.prepare_reply(cmd, reply)

