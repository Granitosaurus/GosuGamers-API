"""
Module for gosugamers.net match data storage and manipulation
"""
from difflib import SequenceMatcher
import re

import requests
from lxml import html

#local

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


class Match:
    """Match class for storing match data"""
    def __init__(self, game, team1, team1_score, team1_bet, team2, team2_score, team2_bet, live_in, tournament, has_vods,
                 match_id, url):

        self.live_in = live_in
        self.tournament = tournament
        self.has_vods = has_vods
        self.match_id = match_id
        self.url = url
        self.game = game or self.extract_game()
        self.team1 = self.fix_team_name(team1, self.game) if '...' in team1 else team1
        self.team1_bet = team1_bet
        self.team1_score = team1_score
        self.team2 = self.fix_team_name(team2, self.game) if '...' in team2 else team2
        self.team2_bet = team2_bet
        self.team2_score = team2_score

    def extract_game(self):
        game = ''.join(re.findall("net/(.*?)/", self.url))
        return game

    @staticmethod
    def fix_team_name(team_name, game):
        """
        Fixes team name if it's shortened by gosugamers.
        e.g. Evil Geniuses sometimes appear as Evil...
        this function will fix it to Evil Geniuses.
        note: requires knownteams_<game_name>.txt to exist
        """
        team_name = team_name.replace('...', '').strip()
        try:
            with open('data/knownteams_{}.txt'.format(game)) as team_file:
                known_teams = team_file.read().splitlines()
                print(known_teams)
        except FileNotFoundError:
            return team_name

        for team in known_teams:
            if team in known_teams:
                return team
        return team_name

    def get_streams(self):
        #TODO test this once some live games are up
        request = requests.get(self.url)
        tree = html.fromstring(request.content)
        streams = tree.xpath("//object[contains(@id, 'live_embed_player_flash')/@data]")
        return streams

    def __dict__(self):
        """Returns dictionary of object data for json storage"""
        data = {
            'game': self.game,
            'team 1': {
                'bet': self.team1_bet,
                'score': self.team1_score
            },
            'team 2': {
                'bet': self.team2_bet,
                'score': self.team2_score
            },
            'live in': self.live_in,
            'tounament': self.tournament,
            'has_vods': self.has_vods,
            'match_id': self.match_id,
            'url': self.url
        }
        return data

    def __str__(self):
        return '{team1} {bet1} vs {bet2} {team2} in: {live_in}' \
               '\n\tScore: {s1} : {s2}' \
               '\n\tTournament: {tour}' \
               '\n\tHas vods: {vods} ' \
               '\n\tmatch id: {match_id}' \
               '\n\turl: {url}' \
               '\n\tgame: {game}' \
            .format(team1=self.team1,
                    bet1=self.team1_bet,
                    team2=self.team2,
                    bet2=self.team2_bet,
                    live_in=self.live_in,
                    s1=self.team1_score,
                    s2=self.team2_score,
                    tour=self.tournament,
                    vods=self.has_vods,
                    match_id=self.match_id,
                    url=self.url,
                    game=self.game)

if __name__ == '__main__':
    print(Match.fix_team_name('Ninjas in ...', 'dota2'))