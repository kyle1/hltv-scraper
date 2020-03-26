import requests
from pyquery import PyQuery as pq

class Team:
    def __init__(self):
        self._team_id = None
        self._team_name = None

        self._get_teams()

    def parse_team(tr):
        print(tr)


class Teams:
    def __init__(self):
        self._teams = None

        self._get_teams()

    def _get_teams(self):
        url = 'https://www.hltv.org/stats/teams'
        #teams_html = pq(url, verify=False)
        teams_html = requests.get(url, verify=False).content
        
        for table in teams_html('table').items():
            print(table.attr['class`'])

teams = Teams()
