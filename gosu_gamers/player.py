"""
Module for gosugamers.net player data storage and manipulation
"""
from gosu_gamers.storage import Storage

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


class Player(Storage):
    """Storage class for Player"""
    def __init__(self, url='', nickname='', fullname='', photo_url='', famous_heroes=''):
        self.nickname = nickname
        self.fullname = fullname
        self.photo_url = photo_url
        self.famous_heroes = famous_heroes
        self.url = url

    def __bool__(self):
        if self.url:
            return True
        else:
            return False

    def __dict__(self):
        """Returns unordered dict of Player data"""
        data = {
            'meta': {
                'url': self.url
            },
            'nickname': self.nickname,
            'fullname': self.fullname,
            'photo url': self.photo_url,
            'famous heroes': self.famous_heroes
        }
        return data

    def __str__(self):
        return repr(self.__dict__())

