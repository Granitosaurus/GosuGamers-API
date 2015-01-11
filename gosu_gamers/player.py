"""
Module for gosugamers.net player data storage and manipulation
"""
import json

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


class Player:
    """Storage class for Player"""
    #TODO add detailed data for a player
    def __init__(self, nickname='', fullname='', photo_url='', famous_heroes='', url=''):
        self.nickname = nickname
        self.fullname = fullname
        self.photo_url = photo_url
        self.famous_heroes = famous_heroes
        self.url = url

    def get_json(self):
        """Returns json"""
        return json.loads(self.__dict__())

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
        return '{nickname} {fullname} {photo} {famous_heroes} {url}'\
            .format(nickname=self.nickname, fullname=self.fullname, photo=self.photo_url,
                    famous_heroes=self.famous_heroes, url=self.url)

