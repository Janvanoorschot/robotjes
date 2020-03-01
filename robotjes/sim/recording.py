class Recording(object):

    def __init__(self):
        self.keyframes = []

    def finalize_keyframe(self, keyframe):
        keyframe['sprite'] = 'r'
        keyframe['src'] = len(self.keyframes)
        keyframe['score'] = len(self.keyframes)


    def forward(self, actual , expected):
        keyframe = {}
        keyframe['action'] = ['f', actual, expected]
        self.finalize(keyframe)

    def backward(self, actual, expected):
        pass

    def right(self, expected):
        pass

    def left(self, expected):
        pass

    def see(self, direction, subject):
        # direction ["left"|"front"|right"]
        # subject ["obstacle"|"clear"|"beacon"|"white"|"black"]
        pass

    def pickUp(self, success):
        pass

    def eatUp(self, success):
        pass

    def putDown(self, success):
        pass

    def paintWhite(self, msg):
        # msg ["success"|"again"]
        pass

    def paintBlack(self, msg):
        pass

    def stopPainting(self, msg):
        pass

    def flipCoin(self):
        pass

    def happy(self):
        pass

    def nonono(self):
        pass




