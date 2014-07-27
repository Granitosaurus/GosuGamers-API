"""
Module for gosugamers.net team data storage and manipulation
"""
import re
import bs4
import requests
#local
from gosu_gamers.meta import DOMAIN
from gosu_gamers.player import Player

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


class Team:
    """Storage class for team data"""
    def __init__(self, name='', country='', rank='', score='', rank_change='', team_id='', url=''):
        self.rank = rank
        self.country = country
        self.name = name
        self.score = score
        self.rank_change = rank_change
        self.team_id = team_id
        self.url = url
        self.team_members = []
        self.manager = None
        self.description = ''

    def get_all_details(self):
        if not self.url:
            self.get_url()
        request = requests.get(self.url)
        soup = bs4.BeautifulSoup(request.content)
        self.description = soup.find('div', id='wiki-content').p.string
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
    print(team.manager)
    print(team.description)
