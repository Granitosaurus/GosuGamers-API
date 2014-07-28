"""
Package for retrieval of team ranks on http://www.gosugamers.net
"""

#local
import re
from gosu_gamers.team import Team
from gosu_gamers.meta import GAMES
#outer
import requests
import bs4

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


class TeamScraper:
    """Scraper for team ranks"""
    def __init__(self, game):
        if game not in GAMES:
            print('game no in ')
            raise AttributeError("parsed games must be one of: {}".format(', '.join(GAMES)))
        self.game = game
        self.teams = []

    def make_dict(self):
        """Returns list of dictionaries for json storage"""
        return [team.make_dict(fill=True) for team in self.teams]

    def get_teams(self):
        """Fills up self.teams with team object with rank, name, country, score and rank_change if possible"""
        request = requests.get('http://www.gosugamers.net/{game}/rankings#team'.format(game=self.game))
        soup = bs4.BeautifulSoup(request.content)
        total_pages = re.findall('=([0-9]+)', soup.find(text='Last').parent.parent['href'])[0]
        total_pages = int(total_pages)
        for page in range(total_pages+1):
            request = requests.get('http://www.gosugamers.net/{game}/rankings?page={page}#team'
                                   .format(game=self.game, page=page))
            soup = bs4.BeautifulSoup(request.content)
            table_rows = soup.find_all('tr', class_='ranking-link')
            for tr in table_rows:
                rank = ''
                try:
                    rank = tr.td.div.string
                    country = tr.find('span', class_='main').span['title']
                    name = tr.find('span', class_='main').text.strip()
                    score = tr.find('td', class_='numbers').string
                    rank_change = tr.find('td', class_='rank-change').i['title']
                    team_id = tr['data-id']
                    self.teams.append(Team(name, country, rank, score, rank_change, team_id))
                except AttributeError:
                    print('failed to get rank:', rank)

    def find_team(self, team):
        if not self.teams:
            self.get_teams()


if __name__ == '__main__':
    #testing
    rc = TeamScraper('dota2')
    rc.get_teams()
    import json
    json_data = json.dumps(rc.make_dict())
    print(json_data)