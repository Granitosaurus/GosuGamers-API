from gosu_gamers.storage import Storage


class Vod(Storage):

    def __init__(self, url, **kwargs):
        self.url = url