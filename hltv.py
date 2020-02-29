import json
import requests
from constants import HLTV_BASE_URL
from lxml import html
from match import Match
from pyquery import PyQuery as pq


results_url = HLTV_BASE_URL + '/results'

#results_html = requests.get(base_url + '/results', verify=False)
results_html = pq(results_url, verify=False)

match_urls = []
for div in results_html('div').items():
    if div.attr['class'] == 'result-con':
        for a in div('a').items():
            match_urls.append(HLTV_BASE_URL + a.attr['href'])

match_urls = [match_urls[0]]  # for testing

for match_url in match_urls:
    match = Match(match_url)
    print(match.dataframe)

    print(match._match_maps.dataframes)
