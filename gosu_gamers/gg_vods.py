from urllib.parse import urljoin
from lxml import html
import re
import requests
from gosu_gamers.match import Match


class VodScraper:

    def __init__(self, team_id='', url=''):
        if not team_id or not url:
            raise NotImplementedError('VodScraper requires either team_id or url')
        self.team_id = team_id
        self.url = url

        if not self.url:
            self.url = self.get_url()
        if not self.team_id:
            self.team_id = self.get_team_id()

        self.body = ''
        self.tree = html.HtmlElement()

    def connect(self):
        """Connects to the url to retrieve the html tree if it's not there"""
        if not len(self.tree):
            self.body = requests.get(self.url).content
            self.tree = html.fromstring(self.body)

    def get_team_id(self):
        if not self.url:
            return ''
        try:
            return re.findall('teams/(\d+)', self.url)[0]
        except IndexError:
            return ''

    def get_url(self):
        return 'http://www.gosugamers.net/dota2/teams/{}-/video-box'.format(self.team_id)

    def get_vods(self, everything=True):
        total_pages = ''.join(self.tree.xpath("//span[contains(text(),'Last')]/../@href"))
        total_pages = re.findall('page=(\d+)', total_pages)
        total_pages = int(total_pages[0]) if total_pages else ''

        for page in range(1, total_pages+1):
            if page == 1:
                body = self.body
                tree = self.tree
            else:
                body = requests.get('{}?page={}'.format(self.url, page)).content
                tree = html.fromstring(body)

            rows = tree.xpath("//table[@class='simple vods']//tr")
            for row in rows:
                url = urljoin(self.url, ''.join(row.xpath(".//td[1]/a/@href")))
                tournament = urljoin(self.url, ''.join(row.xpath(".//td[2]/a/@href")))
                rating = ''.join(row.xpath(".//div[@class='rating']/@title"))
                team1 = ''.join(row.xpath(".//span[contains(@class,'opp1')]/span/text()"))
                team1_flag = ''.join(row.xpath(".//span[contains(@class,'opp1')]/span[contains(@class, 'flag')]/@title"))
                team2 = ''.join(row.xpath(".//span[contains(@class,'opp2')]/span/text()"))
                team2_flag = ''.join(row.xpath(".//span[contains(@class,'opp2')]/span[contains(@class, 'flag')]/@title"))
                match = Match()