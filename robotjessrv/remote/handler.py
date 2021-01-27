import tempfile, os
from multiprocessing.connection import Listener
from subprocess import call

class RemoteHandler(object):

    ROOTDIR=os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

    def __init__(self, host, port, authkey, runscript=f"{ROOTDIR}/bin/runscript"):
        self.host = host
        self.port = port
        self.authkey = authkey
        self.address = (host, port)
        self.runscript = runscript
        self.game_tick = -1

    def run(self, engine, robo_id):
        """ Feed the Engine (read/exec/write)"""
        listener = Listener(self.address)
        con = listener.accept()
        self.game_tick = 0
        while not con.closed:
            try:
                cmd = con.recv()
            except:
                break
            self.game_tick += 1
            engine.game_timer(self.game_tick)
            result = engine.execute(self.game_tick, robo_id, cmd)
            if result:
                try:
                    con.send(result)
                except Exception:
                    break
            else:
                break
        try:
            con.close()
            listener.close()
        except Exception:
            pass

    def run_client(self, script):
        """ run the client in the background (write/read)"""
        fd, path = tempfile.mkstemp(prefix="delete_me_")
        with os.fdopen(fd, 'w') as fp:
            for line in script:
                fp.write(line)
                fp.write("\n")
        command = f"{self.runscript} {self.host} {self.port} {self.authkey} {path} &"
        try:
            call(command, shell=True)
        except Exception:
            pass


