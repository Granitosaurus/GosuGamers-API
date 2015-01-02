"""
Package for the retrieval of matches on http://www.gosugamers.com
"""
import re
from urllib.parse import urljoin

import bs4
import requests
from lxml import html


# local
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
    def __init__(self, game):
        self.game = game
        if game not in GAMES:
            print('game no in ')
            raise AttributeError("parsed games must be one of: {}".format(', '.join(GAMES)))
        self.request = requests.get('http://www.gosugamers.net/{game}/gosubet'.format(game=self.game)).content
        self.tree = html.fromstring(self.request)

    def find_all_matches(self):
        """Finds all matches (live, upcoming, recent)"""
        upcoming = self.find_upcoming_matches()
        live = self.find_live_matches()
        recent = self.find_recent_matches()
        return upcoming + live + recent

    def find_live_matches(self):
        """
        Finds live matches
        :returns list of Match objects
        """
        live_matches = self.tree.xpath('//h2[contains(text(),"Live")]/'
                                           'following-sibling::div[@class="content"]//tr')
        return list(self._find_matches(live_matches))

    def find_upcoming_matches(self):
        """
        Finds upcoming matches
        :returns list of Match objects
        """
        upcoming_matches = self.tree.xpath('//h2[contains(text(),"Upcoming")]/'
                                           'following-sibling::div[@class="content"]//tr')
        return list(self._find_matches(upcoming_matches))

    def find_recent_matches(self):
        """
        Finds recent matches
        :returns list of Match objects
        """
        recent_matches = self.tree.xpath('//h2[contains(text(),"Recent")]/'
                                           'following-sibling::div[@class="content"]//tr')
        return list(self._find_matches(recent_matches))

    def find_all_history(self):
        """Finds match history and fills up self.history_matches list"""
        total_pages = int(re.findall('=([0-9]+)', self.tree.find(text='Last').parent.parent['href'])[0])
        for page in range(2, total_pages+1):
            print('-doing history page {}'.format(page))
            request = requests.get('http://www.gosugamers.net/{game}/gosubet?r-page={page}'.format(game=self.game,
                                                                                                   page=page))
            soup = bs4.BeautifulSoup(request.content)
            matches = soup.find_all('div', class_='content')[2]
            matches = matches.find_all('tr')
            # print(matches)
            yield list(self._find_matches(matches))


    @staticmethod
    def _find_matches(match_trees):
        """
        Static method used by match finders to find matches from
        :param match_trees: list of html trees (usually table rows)
        """
        for match in match_trees:
            # print(match.string)
            team1 = ''.join(match.xpath('.//span[contains(@class,"opp1")]//text()')).strip()
            team2 = ''.join(match.xpath('.//span[contains(@class,"opp2")]//text()')).strip()
            team1_bet = ''.join(match.xpath('.//span[contains(@class,"bet1")]//text()')).strip()
            team2_bet = ''.join(match.xpath('.//span[contains(@class,"bet2")]//text()')).strip()

            match_url = ''.join(match.xpath('.//a[contains(@class,"match")]/@href')).strip()
            match_id = match_url.rsplit('/', 1)[-1].split('-')[0] if match_url else 'not found'
            match_url = urljoin(DOMAIN, match_url)
            live_in = ''.join(match.xpath('.//span[contains(@class,"live-in")]/text()')).strip()

            score = match.xpath('.//span[contains(@class,"score")]//text()')
            team1_score = score[0] if score else ''
            team2_score = score[1] if len(score) > 1 else ''

            tournament = ''.join(match.xpath('.//a[contains(@class,"tournament")]/@href')).strip()
            tournament = urljoin(DOMAIN, tournament)

            has_vods = bool(match.xpath('.//span[contains(@class,"vod")]/img'))
            yield Match(team1, team1_score, team1_bet, team2, team2_score, team2_bet, live_in, tournament,
                                 has_vods, match_id, match_url)

if __name__ == '__main__':
    ms = MatchScraper('dota2')
    print([game.url for game in ms.find_upcoming_matches()])