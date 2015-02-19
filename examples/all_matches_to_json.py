"""
Saves all matches to json file
"""
from datetime import datetime
import json
from gosu_gamers import gg_match


def all_games_to_json():
    ggms = gg_match.MatchScraper()

    live = ggms.find_live_matches()
    upcoming = ggms.find_upcoming_matches()
    recent = ggms.find_recent_matches()
    games_dict = {'live': [m.__dict__() for m in live],
                  'upcoming': [[m.__dict__() for m in upcoming]],
                  'recent': [[m.__dict__() for m in recent]]}

    date = datetime.now().strftime('%Y%m%d%H%M%S')
    with open('all_matches_{}.json'.format(date), 'w') as json_file:
        json_file.write(json.dumps(games_dict))

if __name__ == '__main__':
    all_games_to_json()
