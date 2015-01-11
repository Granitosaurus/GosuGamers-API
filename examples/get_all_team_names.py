__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'

from gosu_gamers import gg_team
from gosu_gamers import meta
from gosu_gamers.utils import name_fixer

if __name__ == '__main__':
    dota2scraper = gg_team.Dota2TeamScraper()
    for team in dota2scraper.get_teams():  # get_teams is a generator
        print(team.name)

    # OR
    # Get stored teams in data
    print(name_fixer.stored_team_names(meta.DOTA2))