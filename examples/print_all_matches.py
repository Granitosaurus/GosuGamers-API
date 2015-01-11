"""
Prints live, upcoming and recent matches of a all games
"""
from gosu_gamers import gg_match


def print_games(what_to_print=None):
    ggms = gg_match.MatchScraper()

    if not what_to_print:
        what_to_print = lambda match: match

    print('Live:')
    for match in ggms.find_live_matches():
        print(what_to_print(match))
    print(''.center(79, '='))

    print('Upcoming:')
    for match in ggms.find_upcoming_matches():
        print(what_to_print(match))
    print(''.center(79, '='))

    print('Recent:')
    for match in ggms.find_recent_matches():
        print(what_to_print(match))
    print(''.center(79, '='))


if __name__ == '__main__':
    print("ONLY TITLES:")
    print_games(what_to_print=lambda match: match.title)
    print("ONLY live in")
    print_games(what_to_print=lambda match: match.live_in)
