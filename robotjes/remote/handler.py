from multiprocessing.connection import Listener


class Handler(object):

    def __init__(self, host, port, authkey, engine):
        address = (host, port)
        self.listener = Listener(address)
        self.engine = engine

    def run(self):
        con = self.listener.accept()
        while not con.closed:
            try:
                cmd = con.recv()
            except EOFError:
                break
            result = self.engine.execute(cmd)
            if result:
                con.send(result)
            else:
                break
        con.close()

