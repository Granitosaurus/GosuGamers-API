from gosu_gamers.gg_match import MatchScraper

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


def example_all_matches():
    """Example that outputs all of the matches from dota2 page"""
    ggms = MatchScraper(game='dota2')
    ggms.find_live_matches()
    ggms.find_upcoming_matches()
    ggms.find_recent_matches()

    print('Live:')
    [print(lm) for lm in ggms.live_matches]
    print(''.center(79, '='))

    print('Upcoming:')
    [print(lm) for lm in ggms.upcoming_matches]
    print(''.center(79, '='))

    print('Recent:')
    [print(lm) for lm in ggms.recent_matches]
    print(''.center(79, '='))

if __name__ == '__main__':
    example_all_matches()