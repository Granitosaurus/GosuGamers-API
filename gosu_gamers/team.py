import json
from urllib.parse import quote, urljoin
from lxml import html
import requests

#local
from gosu_gamers.storage import Storage

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


class Team(Storage):
    """Storage class for team data"""
    def __init__(self, name='', country='', rank='', score='', rank_change='',
                 team_id='', url='', region_rank='', game='', social=None):
        self.world_rank = rank
        self.region_rank = region_rank
        self.country = country
        self.name = name
        self.rating = score
        self.rank_change = rank_change
        self.team_id = team_id
        self.game = game
        self.url = url or self._make_url()
        self.team_members = []
        self.manager = None
        self.social = social

        self.match_history_url = urljoin(self.url, 'matches')
        self.player_history_url = urljoin(self.url, 'player-history')

    def _make_url(self):
        """Makes url to the team's page from team_id and team_name"""
        team_name = quote(self.name)
        return 'http://www.gosugamers.net/{}/teams/{}-{}'.format(self.game, self.team_id, team_name)

    def check_data(self):
        """Checks if all object data is filled in"""
        return all([self.world_rank, self.region_rank, self.country, self.name, self.rating, self.rank_change, self.team_id,
                    self.url, self.team_members, self.manager])

    def get_all_details(self):
        """Fills up details if Team object has an ID does not fill up self.rank_change"""
        request = requests.get(self.url)
        tree = html.fromstring(request.content)
        if not self.rating:
            self.rating = ''.join(tree.xpath('//span[@class="tooltip"]/text()'))
        if not self.world_rank:
            self.world_rank = ''.join(tree.xpath("//div[@class='ranking'][1]/span/text()"))
        if not self.region_rank:
            self.region_rank = ''.join(tree.xpath("//div[@class='ranking'][2]/span/text()"))
        if not self.name:
            self.name = ''.join(tree.xpath("//div[@class='teamNameHolder']/h1/text()")).rsplit('-', 1)[0]
        if not self.country:
            self.country = ''.join(tree.xpath("//div[@class='teamCountry']/span[contains(@class, 'flag')]/@title"))
        if not self.social:
            self.social = tree.xpath("//div[@class='social']/a/@href")

    def __dict__(self, fill=False):
        """
        Returns a formatted unordered dictionary of all team data
        Keyword Arguments:
        fill - if true will try to fill in every element of the Team object before outputting dict. [Default = False]
        """
        data = {
            'meta': {
                'team id': self.team_id,
                'url': self.url,
                'match_history_url': self.match_history_url,
                'player_history_url': self.player_history_url,
            },
            'name': self.name,
            'game': self.game,
            'rank': self.world_rank,
            'region rank': self.region_rank,
            'country': self.country,
            'manager': self.manager,
            'rank change': self.rank_change,
            'region_rank': self.region_rank,
            'world_rank': self.world_rank,
            'rating': self.rating,
            'social': self.social,
            'team members': [p.make_dict() for p in self.team_members]
        }
        return data

    def __str__(self):
        return 'game: {game}\nrank: {rank}\nregion rank: {rrank}\ncountry: {country}\nname: {name}\nscore: {score}' \
               '\nrank change: {rank_change}\n' \
               'team_id: {team_id}\nsocial: {social}\nmatch history: {mhistory}\nplayer history: {phistory}\n' \
               ''\
            .format(rank=self.world_rank, country=self.country, name=self.name, score=self.rating,
                    rank_change=self.rank_change, team_id=self.team_id, game=self.game, social=self.social,
                    mhistory=self.match_history_url, phistory=self.player_history_url, rrank=self.region_rank)

if __name__ == '__main__':
    team = Team(team_id='4387')
    team.get_all_details()
    for member in team.team_members:
        print(member)

    json_data = team.__dict__()
    json_data = json.dumps(json_data)
    print(json_data)
    print(team)
    print(team.url)