import requests
import concurrent.futures
import functools


class RoboRequestor:

    def __init__(self, url):
        self.url = url
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    def list_games(self, cb):
        def my_cb(j):
            if not j or not j['success']:
                cb({})
            else:
                cb(j['list'])
        ftr = self.executor.submit(self.get_url, self.create_url('games'))
        ftr.add_done_callback(functools.partial(self.done_url, my_cb))

    def list_mazes(self, cb):
        def my_cb(j):
            if not j or not j['success']:
                cb({})
            else:
                cb(j['list'])
        ftr = self.executor.submit(self.get_url, self.create_url('mazes'))
        ftr.add_done_callback(functools.partial(self.done_url, my_cb))

    def create_game(self, cb):
        ftr = self.executor.submit(self.post_url, self.create_url('games'))
        ftr.add_done_callback(functools.partial(self.done_url, cb))

    def status_game(self, game_id, cb):
        url = self.create_url(f"games/{game_id}")
        ftr = self.executor.submit(self.get_url, url)
        ftr.add_done_callback(functools.partial(self.done_url, cb))

    # requests support calls
    def create_url(self, path):
        return f"{self.url}{path}"

    def post_url(self, url):
        r = requests.post(url, json = {'size': 13})
        return r.json()

    def get_url(self, url):
        r = requests.get(url)
        return r.json()

    def done_url(self, cb, ftr):
        j = ftr.result()
        if not j:
            j = {}
        cb(j)


