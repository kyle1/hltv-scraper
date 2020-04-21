import pandas as pd
from constants import HLTV_BASE_URL
from datetime import datetime, timedelta
from dateutil import parser
from matchmap import MatchMapBoxscore, MatchMapBoxscores
from pyquery import PyQuery as pq
from time import sleep


class MatchBoxscore:
    def __init__(self, url):
        self._csgo_match_id = None
        self._match_url = None
        self._match_date_time = None
        self._match_description = None
        self._best_of = None
        self._team1_id = None
        self._team1_map_wins = None
        self._team2_id = None
        self._team2_map_wins = None
        self._match_maps = None

        setattr(self, '_csgo_match_id', url.split('/')[-2])
        setattr(self, '_match_url', url)
        setattr(self, '_match_description', url.split('/')[-1])
        self._get_match(url)

    def _get_match(self, url):
        print('Getting match data from ' + url)
        match_html = pq(url, verify=True)
        map_divs = []
        pick_bans = []
        veto_box_count = 0
        for div in match_html('div').items():
            if div.attr['class'] == 'timeAndEvent':
                for sub_div in div('div').items():
                    if sub_div.attr['class'] == 'time':
                        setattr(self, '_match_time', sub_div.text())  # todo- initial loadup has wrong time?
            if div.attr['class'] == 'date':
                date_obj = parser.parse(div.text())
                setattr(self, '_match_date', date_obj.date())
            if div.attr['class'] == 'team1-gradient':
                for a in div('a').items():
                    setattr(self, '_team1_id', a.attr['href'].split('/')[2])
                for sub_div in div('div').items():
                    if sub_div.attr['class'] in ['won', 'lost']:
                        setattr(self, '_team1_map_wins', sub_div.text())
            if div.attr['class'] == 'team2-gradient':
                for a in div('a').items():
                    setattr(self, '_team2_id', a.attr['href'].split('/')[2])
                for sub_div in div('div').items():
                    if sub_div.attr['class'] in ['won', 'lost']:
                        setattr(self, '_team2_map_wins', sub_div.text())
            if div.attr['class'] == 'standard-box veto-box':
                if veto_box_count == 0:
                    best_of_text = div.text()
                    best_of = best_of_text.split()[2]
                    veto_box_count += 1
                    setattr(self, '_best_of', best_of)
                elif veto_box_count == 1:
                    pick_ban_text = div.text()
                    pick_bans = pick_ban_text.splitlines()
                    veto_box_count += 1
            if div.attr['class'] == 'results-center-stats':
                map_divs.append(div)

        hours_into_day = float(self._match_time.split(':')[0]) + float(self._match_time.split(':')[1]) / 60.0

        # print(pick_bans)
        # print(self._match_time)
        # print(hours_into_day)
        dt = date_obj + timedelta(hours=hours_into_day)
        setattr(self, '_match_date_time', dt)

        match_maps = MatchMapBoxscores(self, pick_bans, map_divs)
        setattr(self, '_match_maps', match_maps)

    @property
    def dataframe(self):
        fields_to_include = {
            'CsgoMatchId': self._csgo_match_id,
            'MatchUrl': self._match_url,
            'MatchDateTime': self._match_date_time,
            'MatchDate': self._match_date,
            'MatchTime': self._match_time,
            'MatchDescription': self._match_description,
            'BestOf': self._best_of,
            'Team1Id': self._team1_id,
            'Team1MapWins': self._team1_map_wins,
            'Team2Id': self._team2_id,
            'Team2MapWins': self._team2_map_wins
        }
        return pd.DataFrame([fields_to_include], index=None)

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        dic['MatchDateTime'] = dic['MatchDateTime'].isoformat()
        dic['MatchDate'] = dic['MatchDate'].isoformat()
        dic['MatchMaps'] = self._match_maps.to_dicts
        return dic


class MatchBoxscores:
    def __init__(self):
        self._matches = []

        # self._get_matches()
        self._get_old_matches()  # for past matches

    def __repr__(self):
        return self._matches

    def __iter__(self):
        return iter(self.__repr__())

    def _get_matches(self):
        today = datetime.today().date()
        yesterday = today + timedelta(days=-1)
        d = today + timedelta(days=-1)

        url = 'https://www.hltv.org/results'
        results_html = pq(url, verify=True)
        for div in results_html('div').items():
            if div.attr['class'] == 'results-all':
                for sub_div in div('div').items():
                    found_date_sublist = False
                    if sub_div.attr['class'] == 'results-sublist':
                        # print(sub_div.text())
                        header_text = sub_div.text().splitlines()[0]
                        date_str = header_text.split('for')[1].strip()
                        date_obj = parser.parse(date_str).date()
                        if date_obj == d:
                            print(date_obj)
                            found_date_sublist = True
                    if found_date_sublist:
                        date_sublist_div = sub_div
                        break
                if found_date_sublist:
                    break

        for div in date_sublist_div('div').items():
            if div.attr['class'] == 'result-con':
                for a in div('a').items():
                    match_url = HLTV_BASE_URL + a.attr['href']
                    match = MatchBoxscore(match_url)
                    import requests
                    self._matches.append(match)
                    sleep(10)

    # def _get_old_matches(self):
    #     today = datetime.today().date()
    #     yesterday = today + timedelta(days=-1)
    #     d = today + timedelta(days=-1)
    #     offset = 100
    #     while offset >= 0:
    #         if offset == 0:
    #             url = 'https://www.hltv.org/results'
    #         else:
    #             url = 'https://www.hltv.org/results?offset=' + str(offset)
    #         results_html = pq(url, verify=True)
    #         for div in results_html('div').items():
    #             if div.attr['class'] == 'results-all':
    #                 for sub_div in div('div').items():
    #                     found_date_sublist = False
    #                     if sub_div.attr['class'] == 'results-sublist':
    #                         # print(sub_div.text())
    #                         header_text = sub_div.text().splitlines()[0]
    #                         date_str = header_text.split('for')[1].strip()
    #                         date_obj = parser.parse(date_str).date()
    #                         if date_obj == d:
    #                             print(date_obj)
    #                             found_date_sublist = True
    #                     if found_date_sublist:
    #                         date_sublist_div = sub_div
    #                         break
    #                 if found_date_sublist:
    #                     break

    #     for div in date_sublist_div('div').items():
    #         if div.attr['class'] == 'result-con':
    #             for a in div('a').items():
    #                 match_url = HLTV_BASE_URL + a.attr['href']
    #                 match = MatchBoxscore(match_url)
    #                 import requests
    #                 self._matches.append(match)
    #                 sleep(10)

    @property
    def dataframes(self):
        frames = []
        for match in self.__iter__():
            frames.append(match.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for match in self.__iter__():
            dics.append(match.to_dict)
        return dics
