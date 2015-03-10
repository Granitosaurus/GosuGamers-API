
import re

import requests
from lxml import html
#local
from gosu_gamers.storage import Storage
from gosu_gamers.utils.name_fixer import fix_team_name
from gosu_gamers.utils.processors import first


class Match(Storage):
    """Match class for storing match data"""
    def __init__(self, match_id='', url='', **kwargs):
        self.match_id = match_id or kwargs.get('match_id', '')
        self.url = url or kwargs.get('url', '')

        if not self.match_id and not self.url:
            raise NotImplementedError('Match object creation requires "url" or "match_id"')
        if not self.url:
            self.url = self.get_url()
        if not self.match_id:
            self.match_id = self.get_match_id()

        self.body = ''
        self.tree = html.HtmlElement()

        self.tournament = kwargs.get('tournament', '')
        self.live_in = kwargs.get('live_in', '')
        self.tournament = kwargs.get('tournament', '')
        self.has_vods = kwargs.get('has_vods', '')
        self.game = kwargs.get('game', '') or self.get_game()
        self.team1 = fix_team_name(self.game, kwargs.get('team1', ''))
        self.team1_url = kwargs.get('team1_url', '')
        self.team1_bet = kwargs.get('team1_bet', '')
        self.team1_score = kwargs.get('team1_score', '')
        self.team2 = fix_team_name(self.game, kwargs.get('team2', ''))
        self.team2_url = kwargs.get('team2_url', '')
        self.team2_bet = kwargs.get('team2_bet', '')
        self.team2_score = kwargs.get('team2_score', '')

        self.title = self.get_title()
        self.simple_title = self.get_simple_title()

    def connect(self):
        """Connects to the url to retrieve the html tree if it's not there"""
        if not len(self.tree):
            self.body = requests.get(self.url).content
            self.tree = html.fromstring(self.body)

    def fill_details(self, override_all=False):
        check = lambda element: (not element) or override_all
        if check(self.game):
            self.game = self.get_game()
        if check(self.tournament):
            self.tournament = self.get_tournament()
        if check(self.title):
            self.title = self.get_title()
        if check(self.simple_title):
            self.simple_title = self.get_simple_title()
        if check(self.team1):
            self.team1 = self.get_team1()
        if check(self.team1_url):
            self.team1 = self.get_team1_url()
        if check(self.team2):
            self.team1 = self.get_team2()
        if check(self.team2_url):
            self.team1 = self.get_team2_url()
        # if check()

    def get_team1(self):
        self.connect()
        return first(self.tree.xpath("//div[contains(@class, 'opponent1')]//a/text()"))

    def get_team2(self):
        self.connect()
        return first(self.tree.xpath("//div[contains(@class, 'opponent2')]//a/text()"))

    def get_team1_url(self):
        self.connect()
        return first(self.tree.xpath("//div[contains(@class, 'opponent1')]//a/@href"))

    def get_team2_url(self):
        self.connect()
        return first(self.tree.xpath("//div[contains(@class, 'opponent2')]//a/@href"))

    def get_url(self):
        return "http://www.gosugamers.net/tournaments/-/matches/{}-vs-".format(self.match_id)

    def get_title(self):
        return '{} {} vs {} {}'.format(self.team1, self.team1_bet, self.team2_bet, self.team2)

    def get_simple_title(self):
        return '{} vs {}'.format(self.team1, self.team2)

    def get_tournament(self):
        tournament_id = re.findall('/tournaments/(\d+)', self.url)
        url = 'http://www.gosugamers.net/tournaments/{}--'.format(tournament_id)
        return url

    def get_game(self):
        game = ''.join(re.findall("net/(.*?)/", self.url))
        if game == 'tournaments':
            self.connect()
            game = self.tree.xpath("//div[contains(@class, 'opponent1')]//@href")
            game = game[0] if game else ''
            game = re.findall('/(.*?)/teams', game)
            return game[0] if game else ''
        return game

    def get_match_id(self):
        match_id = ''.join(re.findall("matches/(\d+)", self.url))
        return match_id

    def get_streams(self):
        self.connect()
        streams = self.tree.xpath("//object[contains(@id, 'live_embed_player_flash')]/@data")
        if not streams:
            streams = self.tree.xpath("//div[@id='tab-content-streams']//iframe/@src")
        return streams

    def __dict__(self, get_streams=False):
        """Returns dictionary of object data for json storage"""
        data = {
            'game': self.game,
            'title': self.title,
            'simple_title': self.simple_title,
            'team 1': {
                'name': self.team1,
                'bet': self.team1_bet,
                'score': self.team1_score
            },
            'team 2': {
                'name': self.team2,
                'bet': self.team2_bet,
                'score': self.team2_score
            },
            'live in': self.live_in,
            'tounament': self.tournament,
            'has_vods': self.has_vods,
            'match_id': self.match_id,
            'url': self.url,
        }
        if get_streams:
            data['streams'] = self.get_streams()
        return data

    def __str__(self):
        return repr(self.__dict__())

if __name__ == '__main__':
    m = Match(url='http://www.gosugamers.net/tournaments/5606-/matches/64842-vs-')
    m.get_match_id()
    print(m)