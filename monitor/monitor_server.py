import datetime
import time
from monitor.model import ResponseTime

class MonitorServer:
    def __init__(self, session):
        self.session = session

    def handle(self, msg):
        host = msg.get('host', 'unknown')
        timestamp = msg.get('timestamp', time.time())
        responsetimes = msg.get('responsetimes', {})
        for funname, dict in responsetimes.items():
            count = dict.get("count", 0)
            cummulated = dict.get("cummulated", 0)
            rt = ResponseTime(
                host=host,
                timestamp=datetime.datetime.fromtimestamp(timestamp),
                funname=funname,
                count=count,
                cummulated=cummulated
            )
            self.session.add(rt)
            self.session.commit()

