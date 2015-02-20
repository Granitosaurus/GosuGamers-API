"""
Saves all matches to json file
"""
import json
from gosu_gamers import gg_match


def all_games_to_json(get_streams=True):
    ggms = gg_match.MatchScraper()

    live = ggms.find_live_matches()
    upcoming = ggms.find_upcoming_matches()
    recent = ggms.find_recent_matches()
    games_dict = {'live': [m.__dict__(get_streams=get_streams) for m in live],
                  'upcoming': [m.__dict__(get_streams=get_streams) for m in upcoming],
                  'recent': [m.__dict__(get_streams=get_streams) for m in recent]}

    filename = 'all_matches.json'
    with open(filename, 'w') as json_file:
        print('Saving to "{}"'.format(filename))
        json_file.write(json.dumps(games_dict))

if __name__ == '__main__':
    all_games_to_json()
