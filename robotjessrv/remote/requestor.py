from multiprocessing.connection import Client
from inspect import getframeinfo, stack

class RemoteRequestor(object):

    def __init__(self, host, port, authkey):
        address = (host, port)
        self.conn = Client(address)
        print(f">>RemoteRequestor!!!!!!!!!!!!!!{self.conn}")


    def execute(self, cmd):
        print(f">>execute!!!!!!!!!!!!!!{cmd}")
        caller = getframeinfo(stack()[2][0])
        lineno = caller.lineno
        cmd.insert(0, lineno)
        try:
            self.conn.send(cmd)
            reply = self.conn.recv()
        except Exception as e:
            print(f"!!execute!!!!!!!!!!!!!!{e}")
            reply = None
        print(f"<<execute!!!!!!!!!!!!!!{reply}")
        return reply

    def close(self):
        try:
            self.conn.close()
        except:
            pass
