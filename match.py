import pandas as pd
from constants import HLTV_BASE_URL
from pyquery import PyQuery as pq
from time import sleep


class Match:
    def __init__(self, url):
        self._match_id = None
        self._match_url = None
        self._match_date_time = None
        self._match_description = None
        self._team1_id = None
        self._team2_id = None
        self._match_maps = None

        setattr(self, '_match_id', url.split('/')[-2])
        setattr(self, '_match_url', url)
        setattr(self, '_match_description', url.split('/')[-1])
        self._get_match(url)

    def _get_match(self, url):
        match_html = pq(url, verify=False)
        map_divs = []
        for div in match_html('div').items():
            if div.attr['class'] == 'date':
                setattr(self, '_match_date_time', div.text())
            if div.attr['class'] == 'team1-gradient':
                for a in div('a').items():
                    setattr(self, '_team_one_id', a.attr['href'].split('/')[2])
            if div.attr['class'] == 'team2-gradient':
                for a in div('a').items():
                    setattr(self, '_team_two_id', a.attr['href'].split('/')[2])
            if div.attr['class'] == 'results-center-stats':
                map_divs.append(div)
        match_maps = MatchMaps(self, map_divs)
        setattr(self, '_match_maps', match_maps)

    @property
    def dataframe(self):
        fields_to_include = {
            'MatchId': self._match_id,
            'MatchUrl': self._match_url,
            'MatchDateTime': self._match_date_time,
            'MatchDescription': self._match_description,
            'Team1Id': self._team1_id,
            'Team2Id': self._team2_id
        }
        return pd.DataFrame([fields_to_include], index=None)


class MatchMap:
    def __init__(self, Match, map_number, url):
        self._match_id = None
        self._match_map_number = None
        self._map_name = None
        self._team1_id = None
        self._team2_id = None
        self._team1_rounds_won = None
        self._team1_first_half_side = None
        self._team1_first_half_rounds_won = None
        self._team1_second_half_side = None
        self._team1_second_half_rounds_won = None
        self._team2_rounds_won = None
        self._team2_first_half_side = None
        self._team2_first_half_rounds_won = None
        self._team2_second_half_side = None
        self._team2_second_half_rounds_won = None
        self._player_stats = None

        setattr(self, '_match_id', Match._match_id)
        setattr(self, '_match_map_number', map_number)
        setattr(self, '_team1_id', Match._team1_id)
        setattr(self, '_team2_id', Match._team2_id)
        self._get_match_map_stats(url)

    def _get_match_map_stats(self, url):
        print('Getting match map stats from ' + url)
        map_html = pq(url)
        stats_tables = []
        spans = []
        for div in map_html('div').items():
            if div.attr['class'] == 'match-info-box':
                map_name = div.text().split()[6]
            if div.attr['class'] == 'match-info-row':
                for div in div('div').items():
                    if div.attr['class'] == 'right':
                        for span in div('span').items():
                            spans.append(span)
                        break

        setattr(self, '_map_name', map_name)
        setattr(self, '_team1_rounds_won', spans[0].text())
        setattr(self, '_team2_rounds_won', spans[1].text())
        setattr(self, '_team1_first_half_side', spans[2].attr['class'].split('-')[0])
        setattr(self, '_team1_first_half_rounds_won', spans[2].text())
        setattr(self, '_team2_first_half_side', spans[3].attr['class'].split('-')[0])
        setattr(self, '_team2_first_half_rounds_won', spans[3].text())
        setattr(self, '_team1_second_half_side', spans[4].attr['class'].split('-')[0])
        setattr(self, '_team1_second_half_rounds_won', spans[4].text())
        setattr(self, '_team2_second_half_side', spans[5].attr['class'].split('-')[0])
        setattr(self, '_team1_second_half_rounds_won', spans[5].text())

        for table in map_html('table').items():
            if table.attr['class'] == 'stats-table':
                stats_tables.append(table)

        first_row = True
        for tr in table('tr').items():
            if first_row:
                first_row = False
                continue
            print(tr.text())

    @property
    def dataframe(self):
        fields_to_include = {
            'MatchId': self._match_id,
            'MapNumber': self._match_map_number,
            'MapName': self._map_name,
            'TeamOneRoundsWon': self._team_one_rounds_won,
            'TeamTwoRoundsWon': self._team_two_rounds_won,
            'TeamOneFirstHalfSide': self._team_one_first_half_side,
            'TeamOneFirstHalfRoundsWon': self._team_one_first_half_rounds_won,
            'TeamTwoFirstHalfSide': self._team_two_first_half_side,
            'TeamTwoFirstHalfRoundsWon': self._team_two_first_half_rounds_won,
            'TeamOneSecondHalfSide': self._team_one_second_half_side,
            'TeamOneSecondHalfRoundsWon': self._team_one_second_half_rounds_won,
            'TeamTwoSecondHalfSide': self._team_two_second_half_side,
            'TeamTwoSecondHalfRoundsWon': self._team_two_second_half_rounds_won
        }
        return pd.DataFrame([fields_to_include], index=None)


class MatchMaps:
    def __init__(self, Match, map_divs):
        self._match_maps = []

        self._get_match_maps(Match, map_divs)

    def __repr__(self):
        return self._match_maps

    def __iter__(self):
        return iter(self.__repr__())

    def _get_match_maps(self, Match, map_divs):
        map_number = 1
        for map_div in map_divs:
            for a in map_div('a').items():
                map_url = HLTV_BASE_URL + a.attr['href']
                match_map = MatchMap(Match, map_number, map_url)
                self._match_maps.append(match_map)
                map_number += 1
                sleep(5)

    @property
    def dataframes(self):
        frames = []
        for match_map in self.__iter__():
            frames.append(match_map.dataframe)
        return pd.concat(frames)


class MatchMapPlayerStats:
    def __init__(self):
        self._player_id = None
