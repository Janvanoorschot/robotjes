import uuid

class Robo(object):

    def __init__(self, requestor):
        self.requestor = requestor
        self.id = uuid.uuid4()

    def handle_result(self, result):
        return result

    def handle_boolean_result(self, result):
        # [[UUID('056c5f92-1457-4e45-be8e-32d6f2a18685'), 'paintWhite'], ([[True]],)]
        return result[1][0][0][0]

    def forward(self, steps=1):
        result = self.requestor.execute([self.id, 'forward', steps])
        return self.handle_result(result)

    def backward(self, steps=1):
        result = self.requestor.execute([self.id, 'backward', steps])
        return self.handle_result(result)

    def left(self, steps=1):
        result = self.requestor.execute([self.id, 'left', steps])
        return self.handle_result(result)

    def right(self, steps=1):
        result = self.requestor.execute([self.id, 'right', steps])
        return self.handle_result(result)

    def pickUp(self):
        result = self.requestor.execute([self.id, 'pickUp'])
        return self.handle_result(result)

    def putDown(self):
        result = self.requestor.execute([self.id, 'putDown'])
        return self.handle_result(result)

    def eatUp(self):
        result = self.requestor.execute([self.id, 'eatUp'])
        return self.handle_result(result)

    def paintWhite(self):
        result = self.requestor.execute([self.id, 'paintWhite'])
        return self.handle_result(result)

    def paintBlack(self):
        result = self.requestor.execute([self.id, 'paintBlack'])
        return self.handle_result(result)

    def stopPainting(self):
        result = self.requestor.execute([self.id, 'stopPainting'])
        return self.handle_result(result)

    def leftIsClear(self):
        result = self.requestor.execute([self.id, 'leftIsClear'])
        return self.handle_boolean_result(result)

    def leftIsObstacle(self):
        result = self.requestor.execute([self.id, 'leftIsObstacle'])
        return self.handle_boolean_result(result)

    def leftIsBeacon(self):
        result = self.requestor.execute([self.id, 'leftIsBeacon'])
        return self.handle_boolean_result(result)

    def leftIsWhite(self):
        result = self.requestor.execute([self.id, 'leftIsWhite'])
        return self.handle_boolean_result(result)

    def leftIsBlack(self):
        result = self.requestor.execute([self.id, 'leftIsBlack'])
        return self.handle_boolean_result(result)

    def frontIsClear(self):
        result = self.requestor.execute([self.id, 'frontIsClear'])
        return self.handle_boolean_result(result)

    def frontIsObstacle(self):
        result = self.requestor.execute([self.id, 'frontIsObstacle'])
        return self.handle_boolean_result(result)

    def frontIsBeacon(self):
        result = self.requestor.execute([self.id, 'frontIsBeacon'])
        return self.handle_boolean_result(result)

    def frontIsWhite(self):
        result = self.requestor.execute([self.id, 'frontIsWhite'])
        return self.handle_boolean_result(result)

    def frontIsBlack(self):
        result = self.requestor.execute([self.id, 'frontIsBlack'])
        return self.handle_boolean_result(result)

    def rightIsClear(self):
        result = self.requestor.execute([self.id, 'rightIsClear'])
        return self.handle_boolean_result(result)

    def rightIsObstacle(self):
        result = self.requestor.execute([self.id, 'rightIsObstacle'])
        return self.handle_boolean_result(result)

    def rightIsBeacon(self):
        result = self.requestor.execute([self.id, 'rightIsBeacon'])
        return self.handle_boolean_result(result)

    def rightIsWhite(self):
        result = self.requestor.execute([self.id, 'rightIsWhite'])
        return self.handle_boolean_result(result)

    def rightIsBlack(self):
        result = self.requestor.execute([self.id, 'rightIsBlack'])
        return self.handle_boolean_result(result)

    def message(self, message):
        self.requestor.execute([self.id, 'message', message])
