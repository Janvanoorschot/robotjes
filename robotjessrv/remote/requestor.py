from multiprocessing.connection import Client
from inspect import getframeinfo, stack

class RemoteRequestor(object):

    def __init__(self, host, port, authkey):
        address = (host, port)
        self.conn = None
        self.retries = 0
        while self.conn is None and self.retries < 8:
            try:
                self.conn = Client(address)
            except ConnectionRefusedError as e:
                self.retries = self.retries + 1

    def execute(self, cmd):
        caller = getframeinfo(stack()[2][0])
        lineno = caller.lineno
        cmd.insert(0, lineno)
        try:
            self.conn.send(cmd)
            reply = self.conn.recv()
        except BaseException as e:
            reply = None
        return reply

    def close(self):
        try:
            self.conn.close()
        except BaseException as e:
            pass
