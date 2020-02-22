import uuid

class Robo(object):

    def __init__(self, requestor):
        self.requestor = requestor
        self.id = uuid.uuid4()

    def forward(self, steps=1):
        result = self.requestor.execute([self.id, 'forward', steps])

    def backward(self, steps=1):
        pass

    def left(self, steps=1):
        pass

    def right(self, steps=1):
        pass

    def pickUp(self):
        pass

    def putDown(self):
        pass

    def eatUp(self):
        pass

    def paintWhite(self):
        pass

    def paintBlack(self):
        pass

    def stopPainting(self):
        pass

    def leftIsClear(self):
        pass

    def leftIsBeacon(self):
        pass

    def leftIsWhite(self):
        pass

    def leftIsBlack(self):
        pass

    def frontIsClear(self):
        pass

    def frontIsBeacon(self):
        pass

    def frontIsWhite(self):
        pass

    def frontIsBlack(self):
        pass

    def rightIsClear(self):
        pass

    def rightIsBeacon(self):
        pass

    def rightIsWhite(self):
        pass

    def rightIsBlack(self):
        pass

