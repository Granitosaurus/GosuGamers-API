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


    def get_teams(self):
        """Fills up self.teams with team object with rank, name, country, score and rank_change if possible"""
        request = requests.get(self.url)
        tree = html.fromstring(request.content)
        total_pages = re.findall('page=(\d)', ''.join(tree.xpath("//div[@class='pages']/a[contains(., 'Last')]/@href")))
        total_pages = total_pages[0] if total_pages else 0
        total_pages = int(total_pages)
        for page in range(1, total_pages+1):
            request = requests.get('{}{}{}'.format(self.url, '?page=', page))
            tree = html.fromstring(request.content)
            table_rows = tree.xpath("//tr[contains(@class, 'ranking-link')]")
            for tr in table_rows:
                rank = ''.join(tr.xpath(".//td[@class='rank']/div/text()"))
                country = ''.join(tr.xpath(".//span[contains(@class, 'flag')]/@title"))
                name = ''.join(tr.xpath(".//h4/span/span/text()"))
                score = ''.join(tr.xpath(".//td[@class='numbers']/text()"))
                rank_change = ''.join(tr.xpath(".//td[@class='rank-change']/i/@title"))
                team_id = ''.join(tr.xpath("./@data-id"))
                yield Team(name, country, rank, score, rank_change, team_id, game=self.game)
    # def find_team(self, name=None, country=None, rank_exactly=None, score_exactly=None, rank_change=None, team_id=None,
    #               score_lower=None, score_higher=None, partial_name=None, rank_lower=None, rank_higher=None):
    #     """
    #     Finds a team by provided keyword attributes, returns a list of teams matching the filter settings
    #     Keyword Arguments:
    #     name - exact team name (case insensitive)
    #     country - team origin country
    #     rank_exactly - rank exactly
    #     rank_lower - only teams with lower rank than provided
    #     rank_higher - only teams with higher rank than provided
    #     rank_change - the state of ank change
    #     score_exactly - score exactly
    #     score_lower - only teams with lower score than provided
    #     score_higher - only teams with higher score than provided
    #     team_id = exact team id
    #     partial_name - part of name
    #     """
    #     if not self.teams:
    #         raise AttributeError("Object team list is empty")
    #     results = []
    #     for team in self.teams:
    #         all_args = []
    #         if name is not None:
    #             all_args.append(name.lower() == team.name.lower())
    #         if country is not None:
    #             all_args.append(country.lower() == team.country.lower())
    #         if rank_exactly is not None:
    #             all_args.append(rank_exactly == team.rank)
    #         if rank_higher is not None:
    #             if rank_higher == '':
    #                 all_args.append(rank_higher == team.rank)
    #             else:
    #                 all_args.append(int(rank_higher) > int(team.rank))
    #         if rank_lower is not None:
    #             if rank_lower == '':
    #                 all_args.append(rank_lower == team.rank)
    #             else:
    #                 all_args.append(int(rank_lower) < int(team.rank))
    #         if score_exactly is not None:
    #             all_args.append(score_exactly == team.score)
    #         if rank_change is not None:
    #             all_args.append(rank_change == team.rank_change)
    #         if team_id is not None:
    #             all_args.append(team_id == team.team_id)
    #         if score_higher is not None:
    #             if score_higher == '':
    #                 all_args.append(score_higher == team.score)
    #             else:
    #                 all_args.append(int(score_higher) < int(team.score.replace(',', '')))
    #         if score_lower is not None:
    #             if score_lower == '':
    #                 all_args.append(score_lower == team.score)
    #             else:
    #                 all_args.append(int(score_lower) > int(team.score.replace(',', '')))
    #         if partial_name is not None:
    #             if partial_name == '':
    #                 all_args.append(partial_name == team.name)
    #             else:
    #                 all_args.append(partial_name.lower() in team.name.lower())
    #
    #         if all(all_args):
    #             results.append(team)
    #     return results


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

    print(get_scraper('dota3'))