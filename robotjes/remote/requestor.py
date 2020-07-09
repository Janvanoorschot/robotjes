from multiprocessing.connection import Client
from inspect import getframeinfo, stack

class Requestor(object):

    def __init__(self, host, port, authkey):
        address = (host, port)
        self.conn = Client(address)

    def execute(self, cmd):
        caller = getframeinfo(stack()[2][0])
        lineno = caller.lineno
        cmd.insert(0, lineno)
        try:
            self.conn.send(cmd)
            reply = self.conn.recv()
        except:
            reply = None
        return reply

    def close(self):
        try:
            self.conn.close()
        except:
            pass
