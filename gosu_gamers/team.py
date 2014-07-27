"""
Module for gosugamers.net team data storage and manipulation
"""

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


class Team:
    """Storage class for team data"""
    def __init__(self, name, country='', rank='', score='', rank_change=''):
        self.rank = rank
        self.country = country
        self.name = name
        self.score = score
        self.rank_change = rank_change

    def __str__(self):
        return '{rank} {country} {name} {score} {rank_change}'\
            .format(rank=self.rank, country=self.country, name=self.name, score=self.score, rank_change=self.rank_change)
