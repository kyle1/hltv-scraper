import json
import requests
from lxml import html
from pyquery import PyQuery as pq

base_url = 'http://www.hltv.org'

results_url = base_url + '/results'

#results_html = requests.get(base_url + '/results', verify=False)
results_html = pq(results_url, verify=False)

match_urls = []
for div in results_html('div').items():
    if div.attr['class'] == 'result-con':
        for a in div('a').items():
            match_urls.append(base_url + a.attr['href'])

#for testing:
match_urls = [match_urls[0]]

for match_url in match_urls:
    match_html = pq(match_url, verify=False)
    #print(match_html)
    for div in match_html('div').items():
        # if div.attr['class'] == 'g-grid maps':
        #     print(div)

        # if div.attr['class'] == 'mapholder':
        #     print(div)

        # if div.attr['class'] == 'results-left':
        #     print(div)

        # if 'results-left' in div.attr['class']:
        #     print(div)
        #     print('\n')

        if div.attr['class'] == 'results-center-half-score':
            print(div)
            print('\n')
            for span in div('span').items():
                print(span.text())
                #team_one_first_half_side = span.t