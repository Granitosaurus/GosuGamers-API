import json
from urllib.parse import quote, urljoin
from gosu_gamers.match import Match
from lxml import html
import re
import requests

# local
from gosu_gamers.player import Player
from gosu_gamers.storage import Storage

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


class Team(Storage):
    """Storage class for team data"""
    # Known parameters tuple (attr_name, attr_default)
    schema_name = 'team'

    def __init__(self, team_id='', url='', fill=False, **kwargs):
        super().__init__()
        self.team_id = team_id or kwargs.get('team_id', '')
        self.url = url or kwargs.get('url', '')
        if not self.team_id and not self.url:
            raise NotImplementedError('Team object creation requires "team_id" or "url" fields')
        self.url = self.get_url() if not self.url else self.url
        self.team_id = self.get_team_id() if not self.team_id else self.team_id
        for param, value in self.known_params.items():
            setattr(self, param, kwargs.get(param[0], value['default']))
        self.body = ''
        self.tree = html.HtmlElement()
        if fill:
            self.connect()
            self.fill_details()

    def get_url(self):
        """Makes url to the team's page from team_id and team_name"""
        # team_name = quote(self.name)
        return 'http://www.gosugamers.net/teams/{}-'.format(self.team_id)

    def connect(self):
        """Connects to the url to retrieve the html tree if it's not there"""
        if not len(self.tree):
            self.body = requests.get(self.url).content
            self.tree = html.fromstring(self.body)

    def get_team_id(self):
        if not self.url:
            return ''
        try:
            return re.findall('teams/(\d+)', self.url)[0]
        except IndexError:
            return ''

    def get_match_history_url(self):
        return urljoin(self.url, 'matches')

    def get_player_history_url(self):
        return urljoin(self.url, 'player-history')

    def get_rank_change(self):
        return ''

    def get_country(self):
        self.connect()
        return ''.join(self.tree.xpath("//div[@class='teamCountry']/span[contains(@class, 'flag')]/@title"))

    def get_rating(self):
        self.connect()
        return ''.join(self.tree.xpath('//span[@class="tooltip"]/text()'))

    def get_rank(self):
        self.connect()
        return ''.join(self.tree.xpath("//div[@class='ranking'][1]/span/text()"))

    def get_region_rank(self):
        self.connect()
        return ''.join(self.tree.xpath("//div[@class='ranking'][2]/span/text()"))

    def get_social(self):
        self.connect()
        return self.tree.xpath("//div[@class='social']/a/@href")

    def get_name(self):
        self.connect()
        return ''.join(self.tree.xpath("//div[@class='teamNameHolder']/h1/text()")).rsplit('-', 1)[0].strip()

    def get_game(self):
        self.connect()
        game = self.tree.xpath("//div[@class='teamLinks']//li[1]//@href")
        game = re.findall('/(.*?)/', game[0]) if game else ''
        return ''.join(game)

    def get_icon(self):
        self.connect()
        icon = ''.join(self.tree.xpath('//div[@class="teamImage"]/@style'))
        icon = re.findall("url\(\'(.*?)\'", icon)
        return urljoin(self.url, icon[0]) if icon else ''

    def get_manager(self):
        self.connect()
        try:
            manager = self.tree.xpath("//a[@class='player']")[-1]
        except IndexError:
            return Player()
        if not manager.xpath(".//span[@class='manager']"):  # Check if manager
            return Player()
        photo = manager.xpath(".//div[@class='image']/@style")
        photo = urljoin(self.url, ''.join(re.findall("url\(\'(.*?)\'", photo[0]))) if photo else ''
        nickname = ''.join(manager.xpath(".//h5/text()"))
        fullname = ''.join(manager.xpath(".//span/text()"))
        url = manager.xpath("@href")
        url = urljoin(self.url, url[0]) if url else ''
        return Player(url=url, nickname=nickname, fullname=fullname, photo_url=photo)

    def get_players(self):
        self.connect()
        players = self.tree.xpath("//a[@class='player']")[:5]
        found_players = []
        for player in players:
            photo = player.xpath(".//div[@class='image']/@style")
            photo = urljoin(self.url, ''.join(re.findall("url\(\'(.*?)\'", photo[0]))) if photo else ''
            nickname = ''.join(player.xpath(".//h5/text()"))
            fullname = ''.join(player.xpath(".//span/text()"))
            famous_heroes = player.xpath(".//img[contains(@class, 'hero-icon')]/@title")
            url = player.xpath("@href")
            url = urljoin(self.url, url[0]) if url else ''
            found_players.append(Player(url=url, nickname=nickname, fullname=fullname, photo_url=photo,
                                        famous_heroes=famous_heroes))
        return found_players

    def get_upcoming_matches(self):
        match_links = self.tree.xpath("//table[@id='gb-matches']//a/@href")
        matches = []
        for link in match_links:
            link = urljoin(self.url, link)
            matches.append(Match(url=link, fill=True))
        return matches

    def __dict__(self, fill_details=False, override=False):
        """
        Returns a formatted unordered dictionary of all team data
        Keyword Arguments:
        :param fill_details - if true will try to fill in every element of the Team object before outputting dict.
        :param override - overrides values if argument fill is supplied
        """
        if fill_details:
            self.fill_details(override)
        data = {
            'meta': {
                'team id': self.team_id,
                'url': self.url,
                'match_history_url': self.match_history_url,
                'player_history_url': self.player_history_url,
            },
            'name': self.name,
            'icon': self.icon,
            'game': self.game,
            'rank': self.rank,
            'rank_change': self.rank_change,
            'region rank': self.region_rank,
            'country': self.country,
            'manager': self.manager.dictionary if self.manager else {},
            'rank change': self.rank_change,
            'region_rank': self.region_rank,
            'world_rank': self.rank,
            'rating': self.rating,
            'social': self.social,
            'players': [p.dictionary for p in self.players],
            'upcoming_matches': [m.dictionary for m in self.upcoming_matches]
        }
        return data

    def __str__(self):
        return repr(self.__dict__())


if __name__ == '__main__':
    team = Team(url='http://www.gosugamers.net/dota2/teams/4387-vici-gaming')
    team.fill_details()
    print(team)