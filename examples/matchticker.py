import json
from gosu_gamers.gg_match import MatchScraper
'''
This is example on how to create a matchticker that outputs json file with current match data as a json file.
Comment heavy
'''

#1. we create scraper, in this case we use general scraper that scrapes all games, if you want to scrape specific game
# see <game_name>MatchScraper() objects,i.e. Dota2MatchScraper
match_scraper = MatchScraper()
# find live matches
live_matches = match_scraper.find_live_matches()
# Now live matches have no proper label in matches page, let set it to 'live'
for live_match in live_matches:
    live_match.live_in = 'Live'
# find upcoming matches
upcoming_matches = match_scraper.find_upcoming_matches()

# now we can do whatever we want with that data, in this example lets save all that in json format which can be
# read by our website to display the results

games_dict = {'games': []}
for match in live_matches + upcoming_matches:
    games_dict['games'].append(match.__dict__())  # here we go through every object and save it's __dict__ value
with open('matchticker.json', 'w') as json_file:
    json_file.write(json.dumps(games_dict))