"""
module for the retrieval of matches on http://www.gosugamers.com
"""
from urllib.parse import urljoin

import requests
from lxml import html


# local
from gosu_gamers.match import Match

__author__ = 'rebsadran'


class MatchScraper:
    """
    Base class Match scrapers for gosugamers.com
    Override with url to <game>/gosubet.
    Override game with string of game name, used in match object
    """
    url = 'http://www.gosugamers.net/gosubet'
    domain = 'http://www.gosugamers.net/'
    game = None

    def get_tree(self):
        """
        Downloads page and makes a html tree
        :return: HtmlElement tree
        """
        request = requests.get(self.url)
        tree = html.fromstring(request.content)
        return tree

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
        tree = self.get_tree()
        live_matches = tree.xpath('//h2[contains(text(),"Live")]/'
                                  'following-sibling::div[@class="content"]//tr')
        return list(self._find_matches(live_matches))

    def find_upcoming_matches(self):
        """
        Finds upcoming matches
        :returns list of Match objects
        """
        tree = self.get_tree()
        upcoming_matches = tree.xpath('//h2[contains(text(),"Upcoming")]/'
                                      'following-sibling::div[@class="content"]//tr')
        return list(self._find_matches(upcoming_matches))

    def find_recent_matches(self):
        """
        Finds recent matches
        :returns list of Match objects
        """
        tree = self.get_tree()
        recent_matches = tree.xpath('//h2[contains(text(),"Recent")]/'
                                    'following-sibling::div[@class="content"]//tr')
        return list(self._find_matches(recent_matches))

    def _find_matches(self, match_trees):
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
            match_url = urljoin(self.domain, match_url)
            live_in = ''.join(match.xpath('.//span[contains(@class,"live-in")]/text()')).strip()

            score = match.xpath('.//span[contains(@class,"score")]//text()')
            team1_score = score[0] if score else ''
            team2_score = score[1] if len(score) > 1 else ''

            tournament = ''.join(match.xpath('.//a[contains(@class,"tournament")]/@href')).strip()
            tournament = urljoin(self.domain, tournament)

            has_vods = bool(match.xpath('.//span[contains(@class,"vod")]/img'))
            yield Match(self.game, team1, team1_score, team1_bet, team2, team2_score, team2_bet, live_in, tournament,
                        has_vods, match_id, match_url)

     # def find_all_history(self):
        # """Finds match history and fills up self.history_matches list"""
        #     TODO make this with asyncio or something because it takes ages
        # total_pages = int(re.findall('=([0-9]+)', self.tree.find(text='Last').parent.parent['href'])[0])
        # for page in range(2, total_pages+1):
        #     print('-doing history page {}'.format(page))
        #     request = requests.get('http://www.gosugamers.net/{game}/gosubet?r-page={page}'.format(game=self.game,
        #                                                                                            page=page))
        #     soup = bs4.BeautifulSoup(request.content)
        #     matches = soup.find_all('div', class_='content')[2]
        #     matches = matches.find_all('tr')
        #     print(matches)
        # yield list(self._find_matches(matches))


class CsGoMatchScraper(MatchScraper):
    url = 'http://www.gosugamers.net/counterstrike/gosubet'
    game = 'counterstrike'


class Dota2MatchScraper(MatchScraper):
    url = 'http://www.gosugamers.net/dota2/gosubet'
    game = 'dota2'


class LolMatchScraper(MatchScraper):
    url = 'http://www.gosugamers.net/lol/gosubet'
    game = 'league of legends'


class HearthStoneMatchScraper(MatchScraper):
    url = 'http://www.gosugamers.net/hearthstone/gosubet'
    game = 'hearthstone'


class HotsMatchScraper(MatchScraper):
    url = 'http://www.gosugamers.net/heroesofthestorm/gosubet'
    game = 'heroesofthestorm'


if __name__ == '__main__':
    ms = MatchScraper()
    print([print(game.__str__()) for game in ms.find_live_matches()])