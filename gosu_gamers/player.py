"""
Module for gosugamers.net player data storage and manipulation
"""

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'

class Player:
    """Storage class for Player"""
    def __init__(self, nickname='', fullname='', photo_url='', famous_heroes='', url=''):
        self.nickname = nickname
        self.fullname = fullname
        self.photo_url = photo_url
        self.famous_heroes = famous_heroes
        self.url = url

    def __str__(self):
        return '{nickname} {fullname} {photo} {famous_heroes} {url}'\
            .format(nickname=self.nickname, fullname=self.fullname, photo=self.photo_url,
                    famous_heroes=self.famous_heroes, url=self.url)

