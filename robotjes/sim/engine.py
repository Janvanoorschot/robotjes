LEGAL_COMMANDS = ["forward", "backward", "left", "right", "pickup", "putDown",
                  "eatUp", "paintwhite", "paintBlack", "stopPainting",
                  "leftIsClear", "leftisBeacon", "leftIsWhite", "leftIsBlack",
                  "frontIsClear", "frontisBeacon", "frontIsWhite", "frontIsBlack",
                  "rightIsClear", "rightisBeacon", "rightIsWhite", "rightIsBlack",
                  ]
class Engine(object):

    def __init__(self, map_file):
        self.map_file = map_file

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
        if command == "forward":
            reply = ["forward_reply"]
        elif command == "backward":
            reply = ["backward_reply"]
        elif command == "left":
            reply = ["left_reply"]
        elif command == "right":
            reply = ["right_reply"]
        elif command == "pickup":
            reply = ["pickup_reply"]
        elif command == "putDown":
            reply = ["putDown_reply"]
        elif command == "eatUp":
            reply = ["eatUp_reply"]
        elif command == "paintwhite":
            reply = ["paintwhite_reply"]
        elif command == "paintBlack":
            reply = ["paintBlack_reply"]
        elif command == "stopPainting":
            reply = ["stopPainting_reply"]
        elif command == "leftIsClear":
            reply = ["leftIsClear_reply"]
        elif command == "leftisBeacon":
            reply = ["leftisBeacon_reply"]
        elif command == "leftIsWhite":
            reply = ["leftIsWhite_reply"]
        elif command == "leftIsBlack":
            reply = ["leftIsBlack_reply"]
        elif command == "frontIsClear":
            reply = ["frontIsClear_reply"]
        elif command == "frontisBeacon":
            reply = ["frontisBeacon_reply"]
        elif command == "frontIsWhite":
            reply = ["frontIsWhite_reply"]
        elif command == "frontIsBlack":
            reply = ["frontIsBlack_reply"]
        elif command == "rightIsClear":
            reply = ["rightIsClear_reply"]
        elif command == "rightisBeacon":
            reply = ["rightisBeacon_reply"]
        elif command == "rightIsWhite":
            reply = ["rightIsWhite_reply"]
        elif command == "rightIsBlack":
            reply = ["rightIsBlack_reply"]
        else:
            reply = ["error"]
        return self.prepare_reply(reply)

