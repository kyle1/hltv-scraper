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

print(match_urls)