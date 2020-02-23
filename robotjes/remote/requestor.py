import asyncio

class Requestor(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def execute(self, cmd):
        return cmd
