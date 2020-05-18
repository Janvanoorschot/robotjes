import json

class MonitorServer:
    def __init__(self):
        pass

    def handle(self, msg):
        print(f"handle {json.dumps(msg)}")
