"""
Every x seconds retrieves live match data and prints it out if it hasn't changed from the previous time
run it in your terminal and it will ring the system bell once it's viable (prints '\a')
"""

from gosu_gamers.gg_match import MatchScraper
from time import sleep


def check_dota2():
    dota2 = MatchScraper()
    match_history = []
    while True:
        live_matches = dota2.find_live_matches()
        for game in live_matches:
            if game.match_id not in match_history:
                print('\a', 'Live game found!')
                print('{} ({}) vs {} ({})\n\t-Tournament: {}\n\t-Url: {}'
                      .format(game.team1, game.team1_bet, game.team2, game.team2_bet, game.tournament, game.url))
                match_history.extend([game.match_id for game in live_matches])
                [print('\t-Stream', index, ':', stream) for index, stream in enumerate(game.get_streams())]
        sleep(5)


if __name__ == '__main__':
    check_dota2()

