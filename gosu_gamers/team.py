"""
Module for gosugamers.net team data storage and manipulation
"""
import json
import re
import bs4
import requests
#local
from gosu_gamers.meta import DOMAIN
from gosu_gamers.player import Player

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


class Team:
    """Storage class for team data"""
    def __init__(self, name='', country='', rank='', score='', rank_change='', team_id='', url='', region_rank=''):
        self.rank = rank
        self.region_rank = region_rank
        self.country = country
        self.name = name
        self.score = score
        self.rank_change = rank_change
        self.team_id = team_id
        self.url = url
        self.team_members = []
        self.manager = None
        self.description = ''

    def check_data(self):
        return all([self.rank, self.region_rank, self.country, self.name, self.score, self.rank_change, self.team_id,
                    self.url, self.team_members, self.manager, self.description])

    def get_all_details(self):
        """Fills up details if Team object has an ID does not fill up self.rank_change"""
        if not self.url:
            self.get_url()
        request = requests.get(self.url)
        soup = bs4.BeautifulSoup(request.content)
        try:
            if not self.description:
                self.description = soup.find('div', id='wiki-content').p.string
        except AttributeError:
            self.description = ''
        if not self.score:
            self.score = soup.find('span', class_='tooltip').string
        if not self.rank:
            self.rank = soup.find_all('div', class_='ranking')[0].span.string
        if not self.region_rank:
            self.region_rank = soup.find_all('div', class_='ranking')[0].span.string
        if not self.name:
            self.name = soup.find('div', id='profile-menu').div.h3.string
        if not self.country:
            self.country = soup.find('span', class_='flag')['title']
        #Players
        if not self.team_members:
            players = soup.find_all('a', class_='player')
            for player in players:
                nickname = player.h5.string
                fullname = player.find_all('span')[1].string
                if player.find('span', class_='manager'):
                    manager = True
                else:
                    manager = False
                photo_url = DOMAIN[:-1] + re.findall("\('(.*?)'\)", player.div.attrs['style'])[0]
                famous_heroes = [item['alt'] for item in player.find('div', class_='heroes').find_all('img')]
                url = DOMAIN + player['href']
                if not manager:
                    self.team_members.append(Player(nickname, fullname, photo_url, famous_heroes, url))
                else:
                    self.manager = Player(nickname, fullname, photo_url, famous_heroes, url)

    def make_dict(self, fill=False):
        """
        Returns a formated unordered dictionary of all team data
        Keyword Arguments:
        fill - if true will try to fill in every element of the Team object before outputting dict. [Default = False]
        """
        if fill:
            self.get_all_details()
        try:
            manager = self.manager.make_dict()
        except AttributeError:
            manager = ''
        print('writing json for: #{} {}'.format(self.rank, self.name))
        data = {
            'meta': {
                'team id': self.team_id,
                'url': self.url
            },
            'name': self.name,
            'rank': self.rank,
            'region rank': self.region_rank,
            'country': self.country,
            'manager': manager,
            'desciption': self.description,
            'rank change': self.rank_change,
            'score': self.score,
            'team members': [p.make_dict() for p in self.team_members]
        }
        return data

    def get_url(self, team_id=''):
        """Finds an url to the team's profile from team id"""
        if not team_id:
            if not self.team_id:
                raise AttributeError("team_id not set")
            else:
                team_id = self.team_id

        if not self.url:
            request = requests.get('http://www.gosugamers.net/rankings/show/team/{team_id}'.format(team_id=team_id))
            soup = bs4.BeautifulSoup(request.content)
            url = ''
            try:
                url = DOMAIN + soup.find('div', class_='base').h3.a['href']
            except AttributeError:
                print("Invalid team_id")
            self.url = url
            return self.url

    def __str__(self):
        return '{rank} {country} {name} {score} {rank_change} {team_id}'\
            .format(rank=self.rank, country=self.country, name=self.name, score=self.score,
                    rank_change=self.rank_change, team_id=self.team_id)

if __name__ == '__main__':
    team = Team(team_id='4387')
    team.get_all_details()
    for member in team.team_members:
        print(member)

    json_data = team.make_dict()
    json_data = json.dumps(json_data)
    print(json_data)
    print(team)
    print(team.url)