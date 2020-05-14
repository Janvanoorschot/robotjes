import requests
import concurrent.futures
import json

class RoboRequestor:

    def __init__(self):
        pass

    def list_bubbles(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            ftr = executor.submit(self.load_url, 'http://localhost:8000/bubbles')
            j = ftr.result()
            print(json.dumps(j))

    def load_url(self,url):
        r = requests.get(url)
        return r.json()

