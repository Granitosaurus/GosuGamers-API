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
        for page in range(1, total_pages+1):
            print('-getting team page: {}'.format(page))
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

    def find_team(self, name=None, country=None, rank_exactly=None, score_exactly=None, rank_change=None, team_id=None,
                  score_lower=None, score_higher=None, partial_name=None, rank_lower=None, rank_higher=None):
        """
        Finds a team by provided keyword attributes, returns a list of teams matching the filter settings
        Keyword Arguments:
        name - exact team name (case insensitive)
        country - team origin country
        rank_exactly - rank exactly
        rank_lower - only teams with lower rank than provided
        rank_higher - only teams with higher rank than provided
        rank_change - the state of ank change
        score_exactly - score exactly
        score_lower - only teams with lower score than provided
        score_higher - only teams with higher score than provided
        team_id = exact team id
        partial_name - part of name
        """
        if not self.teams:
            raise AttributeError("Object team list is empty")
        results = []
        for team in self.teams:
            all_args = []
            if name is not None:
                all_args.append(name.lower() == team.name.lower())
            if country is not None:
                all_args.append(country.lower() == team.country.lower())
            if rank_exactly is not None:
                all_args.append(rank_exactly == team.rank)
            if rank_higher is not None:
                if rank_higher == '':
                    all_args.append(rank_higher == team.rank)
                else:
                    all_args.append(int(rank_higher) > int(team.rank))
            if rank_lower is not None:
                if rank_lower == '':
                    all_args.append(rank_lower == team.rank)
                else:
                    all_args.append(int(rank_lower) < int(team.rank))
            if score_exactly is not None:
                all_args.append(score_exactly == team.score)
            if rank_change is not None:
                all_args.append(rank_change == team.rank_change)
            if team_id is not None:
                all_args.append(team_id == team.team_id)
            if score_higher is not None:
                if score_higher == '':
                    all_args.append(score_higher == team.score)
                else:
                    all_args.append(int(score_higher) < int(team.score.replace(',', '')))
            if score_lower is not None:
                if score_lower == '':
                    all_args.append(score_lower == team.score)
                else:
                    all_args.append(int(score_lower) > int(team.score.replace(',', '')))
            if partial_name is not None:
                if partial_name == '':
                    all_args.append(partial_name == team.name)
                else:
                    all_args.append(partial_name.lower() in team.name.lower())

            if all(all_args):
                results.append(team)
        return results


if __name__ == '__main__':
    #testing
    rc = TeamScraper('dota2')
    rc.get_teams()
    search = rc.find_team(rank_higher='')
    for team in search:
        print(team.name, team.rank)