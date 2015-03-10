import json
from urllib.parse import quote, urljoin
from lxml import html
import re
import requests

# local
from gosu_gamers.player import Player
from gosu_gamers.storage import Storage

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


class Team(Storage):
    """Storage class for team data"""

    def __init__(self, team_id='', url='', fill_details=False, **kwargs):
        self.team_id = team_id or kwargs.get('team_id', '')
        self.url = url or kwargs.get('url', '')
        if not self.team_id and not self.url:
            raise NotImplementedError('Team object creation requires "team_id" or "url" fields')

        if not self.url:
            self.url = self.get_url()
        if not self.team_id:
            self.team_id = self.get_team_id()

        self.body = ''
        self.tree = html.HtmlElement()

        self.rank = kwargs.get('rank', '')
        self.region_rank = kwargs.get('region_rank', '')
        self.country = kwargs.get('country', '')
        self.name = kwargs.get('name', '')
        self.rating = kwargs.get('score', '')
        self.rank_change = kwargs.get('rank_change', '')
        self.game = kwargs.get('game', '')
        self.players = kwargs.get('players', [])
        self.manager = kwargs.get('manager', Player())
        self.social = kwargs.get('social', '')
        self.icon = kwargs.get('icon', '')

        self.match_history_url = urljoin(self.url, 'matches')
        self.player_history_url = urljoin(self.url, 'player-history')

        if fill_details:
            self.connect()
            self.fill_details()

    def get_url(self):
        """Makes url to the team's page from team_id and team_name"""
        # team_name = quote(self.name)
        return 'http://www.gosugamers.net/teams/{}-'.format(self.team_id)

    def fill_details(self, override_all=False):
        """Fills up details if Team object has an ID does not fill up self.rank_change"""
        check = lambda element: (not element) or override_all
        if check(self.game):
            self.game = self.get_game()
        if check(self.rating):
            self.rating = self.get_rating()
        if check(self.rank):
            self.rank = self.get_rank()
        if check(self.region_rank):
            self.region_rank = self.get_region_rank()
        if check(self.name):
            self.name = self.get_name()
        if check(self.country):
            self.country = self.get_country()
        if check(self.social):
            self.social = self.get_social()
        if check(self.icon):
            self.icon = self.get_icon()
        if check(self.players):
            self.players = self.get_players()
        if check(self.manager):
            self.manager = self.get_manager()

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

    def get_vods(self):
        self.connect()
        #TODO vods

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
            'region rank': self.region_rank,
            'country': self.country,
            'manager': self.manager.dictionary,
            'rank change': self.rank_change,
            'region_rank': self.region_rank,
            'world_rank': self.rank,
            'rating': self.rating,
            'social': self.social,
            'team members': [p.dictionary for p in self.players]
        }
        return data

    def __str__(self):
        return repr(self.__dict__())


if __name__ == '__main__':
    team = Team(url='http://www.gosugamers.net/dota2/teams/8954-team-secret')
    # print(team.url)
    team.fill_details()
    print(team)
    # print(team.manager)
    # print(team.manager)
    # for member in team.players:
    #     print(member)
    #     print('----------')
    #
    # json_data = team.__dict__()
    # json_data = json.dumps(json_data)
    # print(json_data)

    # print(team)
    # print(team.url)