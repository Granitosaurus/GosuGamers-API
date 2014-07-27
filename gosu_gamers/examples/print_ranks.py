"""
This example prints out all rank data of all available games
"""
from gosu_gamers.gg_team import TeamScraper

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


def pint_all(game):
    ts = TeamScraper(game)
    print(game.center(79, '='))
    ts.get_teams()
    [print(team) for team in ts.teams]
    print('='.center(79, '='))

if __name__ == '__main__':
    pint_all('dota2')
    pint_all('lol')
    pint_all('hearthstone')
