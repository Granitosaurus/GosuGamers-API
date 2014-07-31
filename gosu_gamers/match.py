"""
Module for gosugamers.net match data storage and manipulation
"""

import requests
import bs4
#local
from gosu_gamers.meta import KNOWN_TEAMS

__author__ = 'Bernard @ Bernardas.Alisauskas@gmail.com'


class Match:
    """Match class for storig match data"""
    def __init__(self, team1, team1_score, team1_bet, team2, team2_score, team2_bet, live_in, tournament, has_vods,
                 match_id, url):
        self.team1 = self.fix_team_name(team1)
        self.team1_bet = team1_bet
        self.team1_score = team1_score
        self.team2 = self.fix_team_name(team2)
        self.team2_bet = team2_bet
        self.team2_score = team2_score
        self.live_in = live_in
        self.tournament = tournament
        self.has_vods = has_vods
        self.match_id = match_id
        self.url = url

    @staticmethod
    def fix_team_name(team_name):
        """Fixes team name if it's shortened by gosugamers"""
        for team in KNOWN_TEAMS:
            if team_name.replace('...', '').lower() in team.lower():
                return team
        return team_name

    def get_streams(self):
        request = requests.get(self.url)
        soup = bs4.BeautifulSoup(request.content)
        streams = soup.find_all('object', id='live_embed_player_flash')
        return [stream['data'] for stream in streams]

    def make_dict(self):
        """Returns dictionary of object data for json storage"""
        #TODO update dict output
        data = {
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
            'has_vods': self.has_vods
        }
        return data

    def __str__(self):
        return '{team1} {bet1} vs {bet2} {team2} in: {live_in}' \
               '\n\tScore: {s1} : {s2}' \
               '\n\tTournament: {tour}' \
               '\n\tHas vods: {vods} ' \
               '\n\tmatch id: {match_id}' \
               '\n\turl: {url}'\
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
                    url=self.url)

