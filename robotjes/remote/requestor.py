from multiprocessing.connection import Client


class Requestor(object):

    def __init__(self, host, port, authkey):
        address = (host, port)
        self.conn = Client(address)

    def execute(self, cmd):
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
