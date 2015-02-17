GosuGamers-API
==============

Python unofficial API/Scraper for http://gosugamers.net  
See [Usage](https://github.com/Granitas/GosuGamers-API/#usage) and [examples](https://github.com/Granitas/GosuGamers-API/#example).

#Prerequisites:
Written in Python 3.4  (should work on anything 3+)  
pip install -r requirements.txt or do it manually with pip.  
**lxml** - http://lxml.de/  
>pip install lxml  

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

##Scrapers:
###MatchScraper() object - scraper for gosugamers match pages (i.e. http://www.gosugamers.net/dota2/gosubet)
Scraper for gosugamers matches. Scrapers for games:  
**CsGoMatchScraper** : Counter-Strike: Global offensive match scraper  
**Dota2MatchScraper** : Dota2 match scraper  
**LolMatchScraperr** : League Of Legends match scraper  
**HearthStoneMatchScraper** : Hearthstone match scraper  
**HotsMatchScraperr** : Heroes of the Storm match scraper

Use those to scrape games for matches. All of the scraper objects have these methods that you should use to retrieve results:   
**find\_live\_matches()** - retrieves a list of Match objects of live games.  
**find\_recent\_matches()** - retrieves a list of Match objects of recent games.   
**find\_upcoming\_matches()** - retrieves a list of Match objects of upcoming games.  

**FAQ:**  
Is it possible to retrieve the whole history of matches displayed on gosugamers?  
-Currently the function for that is not available, however

###Match() object - it's a storage object for match data.  
**game** -  game name (i.e. 'dota2').  
**team1** - first team's name (one on the left).  
**team1\_score** - first team's score (if exists).  
**team1\_bet** - first team's bet percentage.  
**team2** -  second team's name (one on the right).  
**team2\_score** - second team's score (if exists).  
**team2\_bet** - second teams bet percentage.  
**live\_in** - live in, unparsed string that is displayed on the webpage (if exists).
**tournament** - tournament name (if exists).
**has\_vods** - True if vods exists otherwise False.  
**match\_id** - Match id used by gosugamers.  
**match\_url** - Direct url to the match page.  

functions:  
**get\_streams()** - returns a list of stream urls found on the match page.
**__dict__()** - returns all data in formatted dict format for easy json output. 
