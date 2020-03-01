from multiprocessing.connection import Client


class Requestor(object):

    def __init__(self, host, port, authkey):
        address = (host, port)
        self.conn = Client(address)

    def execute(self, cmd):
        self.conn.send(cmd)
        reply = self.conn.recv()
        return reply

    def close(self):
        self.conn.close()
