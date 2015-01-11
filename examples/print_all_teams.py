"""
This example prints out all rank data of all available games
"""
from gosu_gamers import gg_team


def print_dota_teams(game, what_to_print=None):
    dota_team_scraper = gg_team.get_scraper(game)

    if not what_to_print:
        what_to_print = lambda team: team

    teams = dota_team_scraper.get_teams()
    for team in teams:
        print(what_to_print(team))

if __name__ == '__main__':
    print_dota_teams('dota2')
