import requests
from match import MatchBoxscore, MatchBoxscores
from player import Players
from schedule import Schedule
from team import Teams


BASE_URL = 'https://localhost:44374/api/'

# players = Players()
# print(players.dataframes)
# response = requests.post(BASE_URL + 'csgo/players', json=players.to_dicts, verify=False).json()
# print(response)

# teams = Teams()
# print(teams.dataframes)
# response = requests.post(BASE_URL + 'csgo/teams', json=teams.to_dicts, verify=False).json()
# print(response)

# schedule = Schedule()
# print(schedule.dataframes)
# response = requests.post(BASE_URL + 'csgo/schedule', json=schedule.to_dicts, verify=False).json()
# print(response)

matches = MatchBoxscores()
matches_df = matches.dataframes
print(matches_df)
print(matches.to_dicts)
response = requests.post(BASE_URL + 'csgo/matches', json=matches.to_dicts, verify=False).json()


#match_boxscore = MatchBoxscore('https://www.hltv.org/matches/2340364/geng-vs-mibr-flashpoint-1')
# print(match_boxscore.dataframe)

#match_maps_df = match_boxscore._match_maps.dataframes
# print(match_maps_df)
# match_maps_df.to_csv('matchmaps.csv')

# print(match_boxscore.to_dict)
#response = requests.post(BASE_URL + 'csgo/matches', json=match)
