$gosugamers-API
========

$gosugamers-API is an unofficial API/Scraper for the gosugamers.net data (matches and teams for now)

Look how easy it is to use:
    from gosu_gamers.gg_team import TeamScraper
    ts = TeamScraper('dota2')
    ts.get_teams()
    [print(team) for team in ts.teams]
    
    # this prints out all dota2 team basic data found on http://www.gosugamers.net/dota2/rankings page, i.e.
    # 1 China NewBee 1,505 Unchanged 7763
    # rank country name score position_change team_id(meta data)

Features
--------

- Scrapes gosugamers.net for match or team details
- Currently supports dota2, lol and hearthstone games

Installation
------------

Install $gosugamers-API by running:

    python install setup.py

Contribute
----------

- Issue Tracker: https://github.com/Granitas/GosuGamers-API/issues
- Source Code: https://github.com/Granitas/GosuGamers-API

Support
-------

If you are having issues, please let me know.

License
-------

The gosugamers-API is licensed under the BSD license.