"""
Package for retrieval of team ranks on http://www.gosugamers.net
"""

#local
import re
from gosu_gamers import meta
from gosu_gamers.team import Team
#outer
import requests
from lxml import html

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


class _TeamScraper:
    """Scraper for team ranks"""
    url = ''
    game = ''

    def get_teams(self, fill_teams=False):
        """Fills up self.teams with team object with rank, name, country, score and rank_change if possible"""
        request = requests.get(self.url)
        tree = html.fromstring(request.content)
        total_pages = re.findall('page=(\d)', ''.join(tree.xpath("//div[@class='pages']/a[contains(., 'Last')]/@href")))
        total_pages = total_pages[0] if total_pages else 0
        total_pages = int(total_pages)
        for page in range(1, total_pages+1):
            request = requests.get('{}?page={}'.format(self.url, page))
            tree = html.fromstring(request.content)
            table_rows = tree.xpath("//tr[contains(@class, 'ranking-link')]")
            for tr in table_rows:
                team_id = ''.join(tr.xpath("./@data-id"))
                if fill_teams:
                    yield Team(team_id=team_id, fill_details=True)
                    continue
                rank = ''.join(tr.xpath(".//td[@class='rank']/div/text()"))
                country = ''.join(tr.xpath(".//span[contains(@class, 'flag')]/@title"))
                name = ''.join(tr.xpath(".//h4/span/span/text()"))
                score = ''.join(tr.xpath(".//td[@class='numbers']/text()"))
                rank_change = ''.join(tr.xpath(".//td[@class='rank-change']/i/@title"))
                yield Team(name=name, country=country, rank=rank, score=score,
                           rank_change=rank_change, team_id=team_id, game=self.game)


class CsGoTeamScraper(_TeamScraper):
    url = 'http://www.gosugamers.net/counterstrike/rankings'
    game = meta.CSGO


class Dota2TeamScraper(_TeamScraper):
    url = 'http://www.gosugamers.net/dota2/rankings'
    game = meta.DOTA2


class LolTeamScraper(_TeamScraper):
    url = 'http://www.gosugamers.net/lol/rankings'
    game = meta.LOL


class HearthstoneTeamScraper(_TeamScraper):
    url = 'http://www.gosugamers.net/hearthstone/rankings'
    game = meta.HEARTHSTONE


class HotsTeamScraper(_TeamScraper):
    url = 'http://www.gosugamers.net/heroesofthestorm/rankings'
    game = meta.HOTS


def get_scraper(game):
    scrapers = {
        meta.DOTA2: Dota2TeamScraper,
        meta.LOL: LolTeamScraper,
        meta.CSGO: CsGoTeamScraper,
        meta.HOTS: HotsTeamScraper,
        meta.HEARTHSTONE: HearthstoneTeamScraper
    }
    if game in scrapers:
        return scrapers[game]()
    else:
        raise AttributeError('Scraper for {} not found\navailable keys: {}'
                             .format(game, scrapers.keys()))

if __name__ == '__main__':
    #testing
    # dota_ts = Dota2TeamScraper()
    # dota_teams = list(dota_ts.get_teams())
    # example_team = dota_teams[1]
    # example_team.get_all_details()
    # print(example_team)

    print(get_scraper('dota2'))