import requests
from pyquery import PyQuery as pq

class Team:
    def __init__(self):
        self._team_id = None
        self._team_name = None

        self._get_teams()

    def parse_team(tr):
        print(tr)

    @property
    def dataframe(self):
        fields_to_include = {
            'CsgoTeamId': self._csgo_team_id,
            'TeamName': self._team_name,
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic

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

    def __repr__(self):
        return self._players

    def __iter__(self):
        return iter(self.__repr__())

    @property
    def dataframes(self):
        frames = []
        for team in self.__iter__():
            frames.append(team.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for team in self.__iter__():
            dics.append(player.to_dict)
        return dics
