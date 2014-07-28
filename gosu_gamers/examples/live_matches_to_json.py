
"""Current match scraper to json

Usage:
    live_matches_to_json.py <game> <file_name>
    live_matches_to_json.py --version
"""
import json
import sys
from gosu_gamers import gg_match


def get_live_matches(game, file_name):
    """
    Outputs live matches
    Keyword arguments:
    game - game name (dota2, lol or hearthstone)
    file_name - output file name
    """
    gosu = gg_match.MatchScraper(game)
    gosu.find_recent_matches()
    if not gosu.recent_matches:
        print("No matches found")
        return ''
    dicts = gosu.recent_make_dict()
    print(dicts)
    json_data = json.dumps(dicts)
    with open(file_name, 'w') as live:
        live.writelines(json_data)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: current_match_to_json.py [dota2|lol|hearthstone] <output_name>')
    else:
        get_live_matches(sys.argv[1], sys.argv[2])



