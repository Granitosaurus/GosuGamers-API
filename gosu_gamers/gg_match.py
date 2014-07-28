"""
Package for the retrieval of matches on http://www.gosugamers.com
"""

import urllib.request
import bs4
import requests

#local
from gosu_gamers.match import Match
from gosu_gamers.meta import GAMES, DOMAIN
__author__ = 'rebsadran'


class MatchScraper:
    """
    Match scraper for gosugamers.com

    Keyword Arguments:
    game - game of which the matches will be scrapped. Choices: dota2,lol,hearthstone (heroes of the storm
    not supported by gosugamers.net yet)
    """
    #TODO implement detailed recent matches
    def __init__(self, game):
        if game not in GAMES:
            print('game no in ')
            raise AttributeError("parsed games must be one of: {}".format(', '.join(GAMES)))
        self.request = requests.get('http://www.gosugamers.net/{game}/gosubet'.format(game=game))
        self.soup = bs4.BeautifulSoup(self.request.content)
        self.all_matches = []
        self.upcoming_matches = []
        self.recent_matches = []
        self.live_matches = []

    def live_make_dict(self):
        """Returns list of dictionaries for json storage"""
        return [match.make_dict() for match in self.live_matches]

    def recent_make_dict(self):
        return [match.make_dict() for match in self.recent_matches]

    def upcoming_make_dict(self):
        return [match.make_dict() for match in self.upcoming_matches]

    def all_make_dict(self):
        return [match.make_dict() for match in self.all_matches]

    def find_all_matches(self):
        self.find_upcoming_matches()
        self.find_live_matches()
        self.find_recent_matches()
        self.all_matches.extend(self.live_matches)
        self.all_matches.extend(self.recent_matches)
        self.all_matches.extend(self.upcoming_matches)

    def find_upcoming_matches(self):
        """Finds upcoming matches and fills up self.upcoming_matches list"""
        upcoming_matches = self.soup.find_all('div', class_='content')[1]
        upcoming_matches = upcoming_matches.find_all('tr')
        self._find_matches(upcoming_matches, self.upcoming_matches)

    def find_recent_matches(self):
        """Finds upcoming matches and fills up self.upcoming_matches list"""
        recent_matches = self.soup.find_all('div', class_='content')[2]
        recent_matches = recent_matches.find_all('tr')
        self._find_matches(recent_matches, self.recent_matches)

    def find_live_matches(self):
        """Finds upcoming matches and fills up self.upcoming_matches list"""
        live_matches = self.soup.find_all('div', class_='content')[0]
        live_matches = live_matches.find_all('tr')
        self._find_matches(live_matches, self.live_matches)

    @staticmethod
    def _find_matches(match_soup, to_list):
        """
        Static method used by match finders to find matches

        Keyword arguments:
        match_soup - bs4.BeautifulSoup object which contains tags of table rows
        to_list - list where the data matches will be saved
        """
        for match in match_soup:
            team1 = match.find('span', class_='opp1').text.strip()
            team1_bet = match.find('span', class_='bet1').text.strip()[1:-1]
            team2 = match.find('span', class_='opp2').text.strip()
            team2_bet = match.find('span', class_='bet2').text.strip()[1:-1]
            try:
                live_in = match.find('span', class_='live-in').text.strip()
            except AttributeError:
                live_in = ""
            try:
                score = match.find_all('span', class_='score')
                team1_score = score[0].text.strip()
                team2_score = score[1].text.strip()
            except (AttributeError, IndexError):
                team1_score = ""
                team2_score = ""
            try:
                tournament = DOMAIN + match.find(class_='tournament').a['href']
            except AttributeError:
                tournament = ""
            try:
                if match.find(class_='vod').img:
                    has_vods = True
                else:
                    has_vods = False
            except AttributeError:
                has_vods = False
            to_list.append(Match(team1, team1_score, team1_bet, team2, team2_score, team2_bet, live_in, tournament,
                                 has_vods))


if __name__ == '__main__':
    pass