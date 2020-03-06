import tempfile, os
from multiprocessing.connection import Listener
from subprocess import call

class Handler(object):

    def __init__(self, host, port, authkey, runscript="bin/runscript"):
        self.host = host
        self.port = port
        self.authkey = authkey
        self.address = (host, port)
        self.runscript = runscript

    def run(self, engine):
        """ Feed the Engine (read/exec/write)"""
        listener = Listener(self.address)
        con = listener.accept()
        while not con.closed:
            try:
                cmd = con.recv()
            except EOFError:
                break
            result = engine.execute(cmd)
            if result:
                con.send(result)
            else:
                break
        con.close()
        listener.close()

    def run_client(self, script):
        """ run the client in the background (write/read)"""
        fd, path = tempfile.mkstemp(prefix="delete_me_")
        with os.fdopen(fd, 'w') as fp:
            for line in script:
                fp.write(line)
        command =  f"{self.runscript} {self.host} {self.port} {self.authkey} {path} &"
        call(command, shell=True)


