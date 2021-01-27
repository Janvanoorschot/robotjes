from multiprocessing.connection import Client
from inspect import getframeinfo, stack

class RemoteRequestor(object):

    def __init__(self, host, port, authkey):
        address = (host, port)
        self.conn = None
        while self.conn is None:
            try:
                self.conn = Client(address)
            except BaseException as e:
                print(f"Client failed: {e}")


    def execute(self, cmd):
        caller = getframeinfo(stack()[2][0])
        lineno = caller.lineno
        cmd.insert(0, lineno)
        try:
            self.conn.send(cmd)
            reply = self.conn.recv()
        except Exception as e:
            reply = None
        return reply

    def close(self):
        try:
            self.conn.close()
        except:
            pass
