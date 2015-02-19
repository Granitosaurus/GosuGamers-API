
import re

import requests
from lxml import html
#local
from gosu_gamers.storage import Storage
from gosu_gamers.utils.name_fixer import fix_team_name


class Match(Storage):
    """Match class for storing match data"""
    def __init__(self, game, team1, team1_score, team1_bet, team2, team2_score, team2_bet, live_in, tournament, has_vods,
                 match_id, url):

        self.live_in = live_in
        self.tournament = tournament
        self.has_vods = has_vods
        self.match_id = match_id
        self.url = url
        self.game = game or self._extract_game()
        self.team1 = fix_team_name(self.game, team1) if '...' in team1 else team1
        self.team1_bet = team1_bet
        self.team1_score = team1_score
        self.team2 = fix_team_name(self.game, team2) if '...' in team2 else team2
        self.team2_bet = team2_bet
        self.team2_score = team2_score

        self.title = '{} {} vs {} {}'.format(team1, team1_bet, team2_bet, team2)
        self.simple_title = '{} vs {}'.format(team1, team2)

    def _extract_game(self):
        game = ''.join(re.findall("net/(.*?)/", self.url))
        return game

    def get_streams(self):
        request = requests.get(self.url)
        tree = html.fromstring(request.content)
        streams = tree.xpath("//object[contains(@id, 'live_embed_player_flash')]/@data")
        if not streams:
            streams = tree.xpath("//div[@id='tab-content-streams']//iframe/@src")
        return streams

    def __dict__(self, get_streams=False):
        """Returns dictionary of object data for json storage"""
        data = {
            'game': self.game,
            'title': self.title,
            'simple_title': self.simple_title,
            'team 1': {
                'name': self.team1,
                'bet': self.team1_bet,
                'score': self.team1_score
            },
            'team 2': {
                'name': self.team2,
                'bet': self.team2_bet,
                'score': self.team2_score
            },
            'live in': self.live_in,
            'tounament': self.tournament,
            'has_vods': self.has_vods,
            'match_id': self.match_id,
            'url': self.url,
        }
        if get_streams:
            data['streams'] = self.get_streams()
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
    pass
    # print(Match.fix_team_name('Ninjas in ...', 'dota2'))