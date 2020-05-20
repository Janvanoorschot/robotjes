from logging import Handler, LogRecord
import socket

class MonitorLogger(Handler):

    def __init__(self, test):
        super().__init__()
        self.hostname = socket.gethostname()

    def emit(self, record: LogRecord):
        from . import mon
        msg = {}
        msg['type'] = 'log'
        msg['host'] = self.hostname
        msg['message'] = record.msg % record.args
        msg['filename'] = record.filename
        msg['lineno'] = record.lineno
        msg['levelname'] = record.levelname
        mon.send_log(msg)
