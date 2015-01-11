GosuGamers-API
==============

Python unofficial API/Scraper for http://gosugamers.net
See examples.

#Prerequisites:
Written in Python 3.4  
pip install -r requirements.txt or do it manually with pip.  
**lxml** - http://lxml.de/  
>pip install beautifulsoup4  
Note: installation might be a bit tricky so please see http://lxml.de/installation.html

**Requests** - https://pypi.python.org/pypi/requests/2.3.0
>pip install requests

#Example:
See examples folder  
i.e.:  
```python
def print_dota_teams(game, what_to_print=None):
    dota_team_scraper = gg_team.get_scraper(game)

    if not what_to_print:
        what_to_print = lambda team: team

    teams = dota_team_scraper.get_teams()
    for team in teams:
        print(what_to_print(team))

if __name__ == '__main__':
    print_dota_teams('dota2')
```


#Usage:

Coming soon.
