import requests
import concurrent.futures
import functools

class RoboRequestor:

    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    def list_bubbles(self, cb):
        ftr = self.executor.submit(self.load_url, 'http://localhost:8000/bubbles')
        ftr.add_done_callback(functools.partial(self.done_url, cb))

    def load_url(self, url):
        r = requests.post(url, json = {'size': 13})
        return r.json()

    def done_url(self, cb, ftr):
        j = ftr.result()
        cb(j)


