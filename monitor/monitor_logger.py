from logging import Handler, LogRecord

class MonitorLogger(Handler):

    def __init__(self, test):
        super().__init__()

    def emit(self, record : LogRecord):
        print("here")
