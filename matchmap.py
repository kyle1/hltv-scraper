import pandas as pd
from constants import HLTV_BASE_URL
from pyquery import PyQuery as pq
from time import sleep


class MatchMapBoxscore:
    def __init__(self, Match, pick_bans, map_number, url):
        self._csgo_match_map_id = None
        self._csgo_match_id = None
        self._match_map_url = None
        self._map_number = None
        self._map_name = None
        self._picked_by_team_id = None
        self._team1_id = None
        self._team1_round_wins = None
        self._team1_first_half_side = None
        self._team1_first_half_round_wins = None
        self._team1_second_half_side = None
        self._team1_second_half_round_wins = None
        self._team1_first_kills = None
        self._team1_kills = None
        self._team1_deaths = None
        self._team1_assists = None
        self._team2_id = None
        self._team2_round_wins = None
        self._team2_first_half_side = None
        self._team2_first_half_round_wins = None
        self._team2_second_half_side = None
        self._team2_second_half_round_wins = None
        self._team2_first_kills = None
        self._team2_kills = None
        self._team2_deaths = None
        self._team2_assists = None

        self._team1_players = None
        self._team2_players = None

        match_map_id = url.split('/')[-2]
        setattr(self, '_csgo_match_map_id', match_map_id)
        setattr(self, '_csgo_match_id', Match._csgo_match_id)
        setattr(self, '_match_map_url', url)
        setattr(self, '_map_number', map_number)
        setattr(self, '_team1_id', Match._team1_id)
        setattr(self, '_team2_id', Match._team2_id)

        self._get_match_map_stats(url, Match, pick_bans, match_map_id)

    def _get_match_map_stats(self, url, Match, pick_bans, match_map_id):
        print('Getting match map stats from ' + url)
        overview_html = pq(url)
        stats_tables = []
        round_win_spans = []
        for div in overview_html('div').items():
            if div.attr['class'] == 'stats-match-maps':
                for a in div('a').items():
                    if 'inactive' not in a.attr['class']:
                        for div in a('div').items():
                            if 'map-name-full' in div.attr['class']:
                                map_name = div.text()
            if div.attr['class'] == 'team-left':
                team1_name = div.text().splitlines()[0]
            if div.attr['class'] == 'team-right':
                team2_name = div.text().splitlines()[0]
            if div.attr['class'] == 'match-info-row':
                for div in div('div').items():
                    if div.attr['class'] == 'right':
                        for span in div('span').items():
                            round_win_spans.append(span)
                        break

        # print(pick_bans)
        # print(team1_name)
        # print(team2_name)

        team_number_picked_map = self._team_picked_map(pick_bans, team1_name, team2_name, map_name)
        if team_number_picked_map == 1:
            picked_by_team_id = Match._team1_id
        elif team_number_picked_map == 2:
            picked_by_team_id = Match._team2_id
        else:
            picked_by_team_id = None

        setattr(self, '_map_name', map_name)
        setattr(self, '_picked_by_team_id', picked_by_team_id)

        # rounds ex: 16:8 (8:7) (8:1) => [16, 8, 8, 7, 8, 1]
        setattr(self, '_team1_round_wins', round_win_spans[0].text())
        setattr(self, '_team1_first_half_side', round_win_spans[2].attr['class'].split('-')[0])
        setattr(self, '_team1_first_half_round_wins', round_win_spans[2].text())
        setattr(self, '_team1_second_half_side', round_win_spans[4].attr['class'].split('-')[0])
        setattr(self, '_team1_second_half_round_wins', round_win_spans[4].text())
        setattr(self, '_team2_round_wins', round_win_spans[1].text())
        setattr(self, '_team2_first_half_side', round_win_spans[3].attr['class'].split('-')[0])
        setattr(self, '_team2_first_half_round_wins', round_win_spans[3].text())
        setattr(self, '_team2_second_half_side', round_win_spans[5].attr['class'].split('-')[0])
        setattr(self, '_team2_second_half_round_wins', round_win_spans[5].text())

        performance_url = url.split('matches')[0] + 'matches/performance' + url.split('matches')[1]
        print('Getting performance stats from ' + performance_url)
        performance_html = pq(performance_url, verify=False)
        for table in performance_html('table').items():
            if table.attr['class'] == 'overview-table':
                row_index = 0
                for tr in table('tr').items():
                    if row_index == 1:
                        # Kills n <graph> m
                        kills_text = tr.text().splitlines()
                        setattr(self, '_team1_kills', kills_text[1])
                        setattr(self, '_team2_kills', kills_text[2])
                    elif row_index == 2:
                        # Deaths n <graph> m
                        deaths_text = tr.text().splitlines()
                        setattr(self, '_team1_deaths', deaths_text[1])
                        setattr(self, '_team2_deaths', deaths_text[2])
                    elif row_index == 3:
                        # Assists n <graph> m
                        assists_text = tr.text().splitlines()
                        setattr(self, '_team1_assists', assists_text[1])
                        setattr(self, '_team2_assists', assists_text[2])
                    row_index += 1

        team1_first_kills, team2_first_kills = self._parse_team_first_kills(performance_html)
        setattr(self, '_team1_first_kills', team1_first_kills)
        setattr(self, '_team2_first_kills', team2_first_kills)

        stats_tables = []
        for table in overview_html('table').items():
            if table.attr['class'] == 'stats-table':
                stats_tables.append(table)
        team1_players = MatchMapPlayersStats(match_map_id, Match._team1_id, stats_tables[0], performance_html)
        team2_players = MatchMapPlayersStats(match_map_id, Match._team2_id, stats_tables[1], performance_html)
        setattr(self, '_team1_players', team1_players)
        setattr(self, '_team2_players', team2_players)

    def _team_picked_map(self, pick_bans, team1_name, team2_name, map_name):
        for decision in pick_bans:
            if map_name in decision:
                if team1_name in decision:
                    return 1
                elif team2_name in decision:
                    return 2
        return None

    def _parse_team_first_kills(self, performance_html):
        team1_first_kills = 0
        team2_first_kills = 0
        for div in performance_html('div').items():
            if div.attr['id'] == 'FIRST_KILL-content':
                first_row = True
                for tr in div('tr').items():
                    if first_row:
                        first_row = False
                        continue
                    first_td = True
                    for td in tr('td').items():
                        if first_td:
                            first_td = False
                            continue
                        for span in td('span').items():
                            if span.attr['class'] == 'team1-player-score':
                                team1_first_kills += int(span.text())
                            else:
                                team2_first_kills += int(span.text())
        return team1_first_kills, team2_first_kills

    @property
    def dataframe(self):
        fields_to_include = {
            'CsgoMatchMapId': self._csgo_match_map_id,
            'CsgoMatchId': self._csgo_match_id,
            'MatchMapUrl': self._match_map_url,
            'MapNumber': self._map_number,
            'MapName': self._map_name,
            'PickedByTeamId': self._picked_by_team_id,
            'Team1Id': self._team1_id,
            'Team1RoundWins': self._team1_round_wins,
            'Team1FirstHalfSide': self._team1_first_half_side,
            'Team1FirstHalfRoundWins': self._team1_first_half_round_wins,
            'Team1SecondHalfRoundWins': self._team1_second_half_round_wins,
            'Team1FirstKills': self._team1_first_kills,
            'Team1Kills': self._team1_kills,
            'Team1Deaths': self._team1_deaths,
            'Team1Assists': self._team1_assists,
            'Team2Id': self._team2_id,
            'Team2RoundWins': self._team2_round_wins,
            'Team2FirstHalfSide': self._team2_first_half_side,
            'Team2FirstHalfRoundWins': self._team2_round_wins,
            'Team2SecondHalfRoundWins': self._team2_second_half_round_wins,
            'Team2FirstKills': self._team2_first_kills,
            'Team2Kills': self._team2_kills,
            'Team2Deaths': self._team2_deaths,
            'Team2Assists': self._team2_assists,
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def player_dataframes(self):
        team1_players = self._team1_players.dataframes
        team2_players = self._team2_players.dataframes
        return pd.concat([team1_players, team2_players])

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        # todo
        # dic['Players'] = blah
        return dic


class MatchMapBoxscores:
    def __init__(self, Match, pick_bans, map_divs):
        self._match_maps = []

        self._get_match_maps(Match, pick_bans, map_divs)

    def __repr__(self):
        return self._match_maps

    def __iter__(self):
        return iter(self.__repr__())

    def _get_match_maps(self, Match, pick_bans, map_divs):
        map_number = 1
        for map_div in map_divs:
            for a in map_div('a').items():
                map_url = HLTV_BASE_URL + a.attr['href']
                match_map = MatchMapBoxscore(Match, pick_bans, map_number, map_url)
                self._match_maps.append(match_map)
                map_number += 1
                sleep(5)

    @property
    def dataframes(self):
        frames = []
        for match_map in self.__iter__():
            frames.append(match_map.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for match_map in self.__iter__():
            dics.append(match_map.to_dict)
        return dics


class MatchMapPlayerStats:
    def __init__(self, tr, match_map_id, team_id):
        self._csgo_player_id = None
        self._csgo_match_map_id = None
        self._csgo_team_id = None
        self._kills = None
        self._assists = None
        self._flash_assists = None
        self._deaths = None
        self._kast = None
        self._adr = None
        self._rating = None
        self._first_kills = None
        self._one_vs_five_wins = None
        self._one_vs_four_wins = None
        self._one_vs_three_wins = None
        self._one_vs_two_wins = None
        self._one_vs_one_wins = None
        self._five_kill_rounds = None
        self._four_kill_rounds = None
        self._three_kill_rounds = None
        self._two_kill_rounds = None
        self._one_kill_rounds = None

        setattr(self, '_csgo_match_map_id', match_map_id)
        setattr(self, '_csgo_team_id', team_id)
        self._parse_player_stats(tr)

    def _parse_player_stats(self, tr):
        for td in tr('td').items():
            if td.attr['class'] == 'st-player':
                for a in td('a').items():
                    player_id = a.attr['href'].split('/')[-2]
                    setattr(self, '_csgo_player_id', player_id)
            elif td.attr['class'] == 'st-kills':
                kills = td.text().split()[0]
                setattr(self, '_kills', kills)
            elif td.attr['class'] == 'st-assists':
                assists = td.text().split()[0]
                flash_assists = td.text().split()[1].replace('(', '').replace(')', '')
                setattr(self, '_assists', assists)
                setattr(self, '_flash_assists', flash_assists)
            elif td.attr['class'] == 'st-deaths':
                deaths = td.text()
                setattr(self, '_deaths', deaths)
            elif td.attr['class'] == 'st-kdratio':  # this is actually KAST
                kast = td.text().replace('%', '')
                setattr(self, '_kast', kast)
            elif td.attr['class'] == 'st-adr':
                adr = td.text()
                setattr(self, '_adr', adr)

    @property
    def dataframe(self):
        fields_to_include = {
            'CsgoPlayerId': self._csgo_player_id,
            'CsgoMatchMapId': self._csgo_match_map_id,
            'CsgoTeamId': self._csgo_team_id,
            'Kills': self._kills,
            'Assists': self._assists,
            'FlashAssists': self._flash_assists,
            'Deaths': self._deaths,
            'Kast': self._kast,
            'Adr': self._adr
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class MatchMapPlayersStats:
    def __init__(self, match_map_id, team_id, stats_table, performance_html):
        self._players = []

        self._get_player_stats(match_map_id, team_id, stats_table, performance_html)

    def __repr__(self):
        return self._players

    def __iter__(self):
        return iter(self.__repr__())

    def _get_player_stats(self, match_map_id, team_id, stats_table, performance_html):
        # stats_tables = []
        # for table in overview_html('table').items():
        #     if table.attr['class'] == 'stats-table':
        #         stats_tables.append(table)

        # team1_stats = stats_tables[0]
        # team2_stats = stats_tables[1]

        first_row = True
        for tr in stats_table('tr').items():
            if first_row:
                first_row = False  # Skip header row
                continue
            player_stats = MatchMapPlayerStats(tr, match_map_id, team_id)
            self._players.append(player_stats)

        # first_row = True
        # for tr in team2_stats('tr').items():
        #     if first_row:
        #         first_row = False  # Skip header row
        #         continue
        #     player_stats = MatchMapPlayerStats(tr, match_map_id, Match._team2_id)
        #     self._team2_players.append(player_stats)

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
