import requests
from pyquery import PyQuery as pq


class Player:
    def __init__(self, tr):
        self._player_id = None
        self._player_name = None
        self._team_id = None

    def _parse_player(self, tr):
        for td in tr('td').items():
            if 'player' in td.attr['class']:
                setattr(self, '_player_name', td.text())
                for a in td('a').items():
                    player_url = a.attr['href']
                    player_id = player_url.split('/')[3]
                    setattr(self, '_player_id', player_id)

    @property
    def dataframe(self):
        fields_to_include = {
            'CsgoPlayerId': self._csgo_player_id,
            'PlayerName': self._player_name,
            'CsgoTeamId': self._csgo_team_id,
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class Players:
    def __init__(self):
        self._players = []

        self._get_players()

    def __repr__(self):
        return self._players

    def __iter__(self):
        return iter(self.__repr__())

    def _get_players(self):
        url = 'https://www.hltv.org/stats/players?startDate=all'
        players_html = pq(url, verify=False, proxies={'http':'50.192.195.69'})
        #players_html = requests.get(url, verify=False).content
        for table in players_html('table').items():
            first_row = True
            for tr in table('tr').items():
                if first_row:
                    first_row = False
                    continue
                player = Player(tr)
                self._players.append(player)

    @property
    def dataframes(self):
        frames = []
        for player in self.__iter__():
            frames.append(player.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for player in self.__iter__():
            dics.append(player.to_dict)
        return dics

