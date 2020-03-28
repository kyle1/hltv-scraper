from pyquery import PyQuery as pq


class Player:
    def __init__(self):
        self._player_id = None
        self._player_name = None
        self._team_id = None


class Players:
    def __init__(self):
        self._players = []

        self._get_players()

    def _get_players(self):
        url = 'https://www.hltv.org/stats/players?startDate=all'
        players_html = pq(url, verify=False)
        for table in players_html('table').items():
            first_row = True
            for tr in table('tr').items():
                if first_row:
                    first_row = False
                    continue
                for td in tr('td').items():
                    if 'player' in td.attr['class']:
                        print(td.text())
                        for a in td('a').items():
                            player_url = a.attr['href']
                            player_id = player_url.split('/')[3]
                            print(player_id)
