import datetime
import time
from monitor.model import ResponseTime, ErrorMessage, LogMessage

class MonitorServer:
    def __init__(self, session):
        self.session = session

    def handle(self, msg):
        if not 'type' in msg:
            return self.handle_unknown(msg)
        elif msg['type'] == 'responsetime':
            return self.handle_responsetime(msg)
        elif msg['type'] == 'log':
            return self.handle_log(msg)
        else:
            return self.handle_unknown(msg)

    def handle_responsetime(self, msg):
        host = msg.get('host', 'unknown')
        process = msg.get('process', 0)
        thread = msg.get('thread', 0)
        timestamp = msg.get('timestamp', time.time())
        responsetimes = msg.get('responsetimes', {})
        for funname, dict in responsetimes.items():
            count = dict.get("count", 0)
            cummulated = dict.get("cummulated", 0)
            rt = ResponseTime(
                host=host,
                process=process,
                thread=thread,
                timestamp=datetime.datetime.fromtimestamp(timestamp),
                funname=funname,
                count=count,
                cummulated=cummulated
            )
            self.session.add(rt)
            self.session.commit()

    def handle_log(self, msg):
        host = msg.get('host', 'unknown')
        process = msg.get('process', 0)
        thread = msg.get('thread', 0)
        timestamp = time.time()
        message = msg.get('message', 'unknown')
        filename = msg.get('filename', 'unknown')
        lineno = msg.get('lineno', 0)
        levelname = msg.get('levelname', 'unknown')
        lm = LogMessage(
            host=host,
            process=process,
            thread=thread,
            timestamp=datetime.datetime.fromtimestamp(timestamp),
            message=message,
            filename=filename,
            lineno=lineno,
            levelname=levelname
        )
        self.session.add(lm)
        self.session.commit()

    def handle_unknown(self, msg):
        timestamp = time.time()
        type = msg.get('type', 'unknown')
        message = msg.get('message', 'unknown')
        em = ErrorMessage(
            timestamp=datetime.datetime.fromtimestamp(timestamp),
            type=type,
            message=message
        )
        self.session.add(em)
        self.session.commit()

