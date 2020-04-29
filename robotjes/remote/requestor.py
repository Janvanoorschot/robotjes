from multiprocessing.connection import Client


class Requestor(object):

    def __init__(self, host, port, authkey):
        address = (host, port)
        self.conn = Client(address)

    def execute(self, cmd):
        self.conn.send(cmd)
        try:
            reply = self.conn.recv()
        except:
            reply = None
        return reply

    def close(self):
        self.conn.close()
