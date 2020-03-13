import json

class Recording(object):

    def __init__(self):
        self.keyframes = []

    def finalize(self, keyframe):
        keyframe['sprite'] = 'r'
        keyframe['src'] = len(self.keyframes)
        keyframe['score'] = len(self.keyframes)
        self.keyframes.append(keyframe)

    def toMap(self):
        result = []
        for item in self.keyframes:
            result.append(item)
        return result

    def isSuccess(self):
        """ we assume success if there are no messages """
        for frame in self.keyframes:
            if frame["action"][0] == 'message':
                return False
        return True

    def messages(self):
        result = []
        for frame in self.keyframes:
            if frame["action"][0] == 'message':
                result.append({
                    "msg": frame["action"][1],
                    "type": "error",
                    "line": 1
                })
        return result


    def forward(self, actual , expected):
        keyframe = {}
        keyframe['action'] = ['f', actual, expected]
        self.finalize(keyframe)

    def backward(self, actual, expected):
        keyframe = {}
        keyframe['action'] = ['b', actual, expected]
        self.finalize(keyframe)

    def left(self, actual):
        keyframe = {}
        keyframe['action'] = ['l', actual]
        self.finalize(keyframe)

    def right(self, actual):
        keyframe = {}
        keyframe['action'] = ['r', actual]
        self.finalize(keyframe)

    def see(self, direction, subject):
        # direction ["left"|"front"|right"]
        # subject ["obstacle"|"clear"|"beacon"|"white"|"black"]
        keyframe = {}
        keyframe['action'] = ['s', direction, subject]
        self.finalize(keyframe)

    def pickUp(self, success):
        keyframe = {}
        if success:
            keyframe['action'] = ['gg', "success"]
        else:
            keyframe['action'] = ['gg', "failure"]
        self.finalize(keyframe)

    def eatUp(self, success):
        keyframe = {}
        if success:
            keyframe['action'] = ['ge', "success"]
        else:
            keyframe['action'] = ['ge', "failure"]
        self.finalize(keyframe)

    def putDown(self, success):
        keyframe = {}
        if success:
            keyframe['action'] = ['gp', "success"]
        else:
            keyframe['action'] = ['gp', "failure"]
        self.finalize(keyframe)

    def paintWhite(self, start):
        # msg ["success"|"again"]
        keyframe = {}
        if start:
            keyframe['action'] = ['pw', "success"]
        else:
            keyframe['action'] = ['pw', "again"]
        self.finalize(keyframe)

    def paintBlack(self, start):
        keyframe = {}
        if start:
            keyframe['action'] = ['pb', "success"]
        else:
            keyframe['action'] = ['pb', "again"]
        self.finalize(keyframe)

    def stopPainting(self):
        keyframe = {}
        keyframe['action'] = ['sp', "success"]
        self.finalize(keyframe)

    def flipCoin(self):
        keyframe = {}
        keyframe['action'] = ['fp']
        self.finalize(keyframe)

    def happy(self):
        keyframe = {}
        keyframe['action'] = ['happy']
        self.finalize(keyframe)

    def nonono(self):
        keyframe = {}
        keyframe['action'] = ['nonono']
        self.finalize(keyframe)

    def message(self, message):
        keyframe = {}
        keyframe['action'] = ['message', message]
        self.finalize(keyframe)

    def boom(self, cmd):
        keyframe = {}
        keyframe['action'] = ['boom', json.dumps(cmd, default=str)]
        self.finalize(keyframe)




