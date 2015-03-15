
import re

import requests
from lxml import html
#local
from gosu_gamers.storage import Storage
from gosu_gamers.utils.name_fixer import fix_team_name
from gosu_gamers.utils.processors import first


class Match(Storage):
    """Match class for storing match data"""
    schema_name = 'match'

    def __init__(self, match_id='', url='', fill=False, **kwargs):
        super().__init__()
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
        for param, value in self.known_params.items():
            setattr(self, param, kwargs.get(param[0], value['default']))

        self.body = ''
        self.tree = html.HtmlElement()
        if fill:
            self.connect()
            self.fill_details()

    def connect(self):
        """Connects to the url to retrieve the html tree if it's not there"""
        if not len(self.tree):
            self.body = requests.get(self.url).content
            self.tree = html.fromstring(self.body)

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

    def get_team1_bet(self):
        return ''

    def get_team2_bet(self):
        return ''

    def get_team1_score(self):
        self.connect()
        return first(self.tree.xpath("//span[contains(@class, 'results')]/span[1]/text()"))

    def get_team2_score(self):
        self.connect()
        return first(self.tree.xpath("//span[contains(@class, 'results')]/span[2]/text()"))

    def get_draw_bet(self):
        return ''

    def get_has_vods(self):
        return ''

    def get_url(self):
        return "http://www.gosugamers.net/tournaments/-/matches/{}-vs-".format(self.match_id)

    def get_title(self):
        if all((self.team1, self.team2)):
            if self.team1_bet and self.team2_bet:
                return '{} {} vs {} {}'.format(self.team1, self.team1_bet, self.team2_bet, self.team2)
            else:
                '{} vs {}'.format(self.team1, self.team2)
        return ''

    def get_simple_title(self):
        return '{} vs {}'.format(self.team1, self.team2) if (self.team1 and self.team2) else ''

    def get_tournament(self):
        tournament_id = re.findall('/tournaments/(\d+)', self.url)
        if tournament_id:
            url = 'http://www.gosugamers.net/tournaments/{}--'.format(tournament_id[0])
            return url
        return ''

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

    def get_live_in(self):
        return ''

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
    m = Match(url='http://www.gosugamers.net/dota2/tournaments/5971-starladder-season-12/1576-phase-1-china/5980-group-a/matches/69094-invictus-gaming-vs-lgd')
    print(m)
    print(m.get_team1())
    print(m.get_team1_bet())
    print(m.get_team2())
    print(m.get_team2_bet())
    m.fill_details()
    print(m)