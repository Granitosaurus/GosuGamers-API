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

    def get_teams(self):
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
                try:
                    rank = tr.td.div.string
                    country = tr.find('span', class_='main').span['title']
                    name = tr.find('span', class_='main').text.strip()
                    score = tr.find('td', class_='numbers').string
                    rank_change = tr.find('td', class_='rank-change').i['title']
                    self.teams.append(Team(name, country, rank, score, rank_change))
                except AttributeError:
                    print('failed to get rank:', rank)


if __name__ == '__main__':
    rc = TeamScraper('hearthstone')
    rc.get_teams()
    for r in rc.teams:
        print(r)