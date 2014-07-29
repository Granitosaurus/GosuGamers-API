__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'

from gosu_gamers.gg_team import TeamScraper

def all_teams(game, file_name=None):
    ts = TeamScraper(game)
    ts.get_teams()