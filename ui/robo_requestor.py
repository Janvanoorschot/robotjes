import requests
import concurrent.futures
import functools


class RoboRequestor:

    def __init__(self, url):
        self.url = url
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    def list_games(self, cb):
        def my_cb(j):
            cb(j)
            # if not j or not j['success']:
            #     cb({})
            # else:
            #     cb(j['list'])
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

    def create_game(self, cb, spec):
        ftr = self.executor.submit(self.post_url, self.create_url('games'), spec)
        ftr.add_done_callback(functools.partial(self.done_url, cb))

    def delete_game(self, cb, spec):
        game_id = spec.get('game_id', "unknown")
        umpire_id = spec.get('umpire_id', "unknown")
        ftr = self.executor.submit(self.delete_url, self.create_url(f"games/{game_id}/{umpire_id}"), spec)
        ftr.add_done_callback(functools.partial(self.done_url, cb))

    def register_player(self, cb, spec):
        game_id = spec['game_id']
        del(spec['game_id'])
        ftr = self.executor.submit(self.put_url, self.create_url(f"games/{game_id}"), spec)
        ftr.add_done_callback(functools.partial(self.done_url, cb))

    def status_game(self, game_id, cb):
        url = self.create_url(f"games/{game_id}")
        ftr = self.executor.submit(self.get_url, url)
        ftr.add_done_callback(functools.partial(self.done_url, cb))

    # requests support calls
    def create_url(self, path):
        return f"{self.url}{path}"

    def post_url(self, url, data):
        try:
            r = requests.post(url, json = data)
            if r.status_code == 200:
                return r.json()
            else:
                return {}
        except:
            return {}

    def put_url(self, url, data):
        try:
            r = requests.put(url, json = data)
            if r.status_code == 200:
                return r.json()
            else:
                return {}
        except:
            return {}

    def get_url(self, url):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.json()
            else:
                return {}
        except:
            return {}

    def delete_url(self, url):
        try:
            r = requests.delete(url)
            if r.status_code == 200:
                return r.json()
            else:
                return {}
        except:
            return {}

    def done_url(self, cb, ftr):
        j = ftr.result()
        cb(j)
