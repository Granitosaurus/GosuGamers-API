import urllib.request
import bs4
import requests
__author__ = 'rebsadran'

KNOWN_TEAMS = ["Natus'Vincere", "Evil Geniuses"]
DOMAIN = 'http://www.gosugamers.net/'


class MatchScraper:
    """#TODO set docstring"""
    def __init__(self):
        self.request = requests.get('http://www.gosugamers.net/dota2/gosubet')
        self.soup = bs4.BeautifulSoup(self.request.text)
        self.all_match_list = []
        self.upcoming_matches = []
        self.recent_matches = []

    def find_upcoming_matches(self):
        upcoming_matches = self.soup.find_all('div', class_='content')[1]
        upcoming_matches = upcoming_matches.find_all('tr')
        self._find_matches(upcoming_matches, self.upcoming_matches)

    def find_recent_matches(self):
        recent_matches = self.soup.find_all('div', class_='content')[2]
        recent_matches = recent_matches.find_all('tr')
        self._find_matches(recent_matches, self.recent_matches)

    def find_live_matches(self):
        live_matches = self.soup.find_all('div', class_='content')[0]
        live_matches = live_matches.find_all('tr')
        self._find_matches(live_matches, self.recent_matches)

    def _find_matches(self, match_soup, to_list):
        for match in match_soup:
            team1 = match.find('span', class_='opp1').text.strip()
            team1_bet = match.find('span', class_='bet1').text.strip()[1:-1]
            team2 = match.find('span', class_='opp2').text.strip()
            team2_bet = match.find('span', class_='bet2').text.strip()[1:-1]
            try:
                live_in = match.find('span', class_='live-in').text.strip()
            except AttributeError:
                live_in = ""
            try:
                score = match.find_all('span', class_='score')
                team1_score = score[0].text.strip()
                team2_score = score[1].text.strip()
            except AttributeError:
                team1_score = ""
                team2_score = ""
            try:
                tournament = DOMAIN + match.find(class_='tournament').a['href']
            except AttributeError:
                tournament = ""
            if match.find(class_='vod').img:
                has_vods = True
            else:
                has_vods = False
            to_list.append(Match(team1, team1_score, team1_bet, team2, team2_score, team2_bet, live_in, tournament,
                                 has_vods))


class Match:
    """Match class """
    def __init__(self, team1, team1_score, team1_bet, team2, team2_score, team2_bet, live_in, tournament, has_vods):
        self.team1 = self.fix_team_name(team1)
        self.team1_bet = team1_bet
        self.team1_score = team1_score
        self.team2 = self.fix_team_name(team2)
        self.team2_bet = team2_bet
        self.team2_score = team2_score
        self.live_in = live_in
        self.tournament = tournament
        self.has_vods = has_vods

    @staticmethod
    def fix_team_name(team_name):
        for team in KNOWN_TEAMS:
            if team_name.replace('...', '').lower() in team.lower():
                return team
        return team_name

    def __str__(self):
        return '{team1} {bet1} vs {bet2} {team2} in: {live_in}\n\tScore: {s1} : {s2}\n\tTournament: {tour}\n\t' \
               'Has vods: {vods}'\
            .format(team1=self.team1, bet1=self.team1_bet, team2=self.team2, bet2=self.team2_bet, live_in=self.live_in,
                    s1=self.team1_score, s2=self.team2_score, tour=self.tournament, vods=self.has_vods)



if __name__ == '__main__':
    ggms = MatchScraper()
    # ggms.find_upcoming_matches()
    # ggms.find_live_matches()
    ggms.find_recent_matches()
    print(len(ggms.recent_matches))