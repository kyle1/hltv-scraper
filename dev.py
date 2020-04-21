import requests
from event import Event, Events
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

# events = Events()
# print(events.dataframes)
# print(events.to_dicts)
# response = requests.post(BASE_URL + 'csgo/events', json=events.to_dicts, verify=False).json()
# print(response)

schedule = Schedule()
# print(schedule.dataframes)
#response = requests.post(BASE_URL + 'csgo/schedule', json=schedule.to_dicts, verify=False).json()
# print(response)

# matches = MatchBoxscores()
# matches_df = matches.dataframes
# print(matches_df)
# print(matches.to_dicts)
# response = requests.post(BASE_URL + 'csgo/matches', json=matches.to_dicts, verify=False).json()

# match = MatchBoxscore('https://www.hltv.org/matches/2340574/rozu-vs-draconic-esea-mdl-season-33-australia-relegation')
# print(match.to_dict)

# matches = MatchBoxscores()
# for match in matches._matches:
#     for map in match._match_maps:
#         player_stats_df = map.player_dataframes
#         print(player_stats_df)
