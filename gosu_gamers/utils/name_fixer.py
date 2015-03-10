import pkg_resources
import requests
from lxml import html
from gosu_gamers import meta

"""
This module is for fixing mangled team names
"""

def update_teamsfile(game):
    teams = []
    page = 1
    while True:
        content = requests.get('http://www.gosugamers.net/{}/rankings?page={}'.format(game, page)).content
        tree = html.fromstring(content)
        next_page_href = tree.xpath("//span[contains(text(),'Next')]/parent::a/@href")
        found_teams = tree.xpath(".//h4/span/span/text()")
        teams.extend(found_teams)
        if next_page_href:
            page = next_page_href[0].split('page=')[-1]
        else:
            break
    with open('data/knownteams_{}.txt'.format(game), 'w') as team_file:
            for t in teams:
                team_file.write(t + '\n')
    return teams


def stored_team_names(game):
    try:
        team_file_data = pkg_resources.resource_string('gosu_gamers', 'data/knownteams_{}.txt'.format(game))
        known_teams = team_file_data.decode().splitlines()
    except FileNotFoundError:
        print('knownteams file in data folder for game {} not found'.format(game))
        return None
    return known_teams


def fix_team_name(game, team_name):
    """
    Fixes team name if it's shortened by gosugamers.
    e.g. Evil Geniuses sometimes appear as Evil...
    this function will fix it to Evil Geniuses.
    note: requires knownteams_<game_name>.txt to exist
    """
    if '...' not in team_name:
        return team_name
    team_name_fixed = team_name.replace('...', '').strip()
    known_teams = stored_team_names(game) or team_name  # if failed

    for team in known_teams:
        if team_name_fixed in team:
            return team
    return team_name_fixed

if __name__ == '__main__':
    print(fix_team_name(meta.DOTA2, 'Hellraisers...'))