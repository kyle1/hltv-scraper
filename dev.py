import requests
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

schedule = Schedule()
print(schedule.dataframes)
schedule_df = schedule.dataframes

print(schedule_df)
print(schedule.to_dicts)

response = requests.post(BASE_URL + 'csgo/schedule', json=schedule.to_dicts, verify=False).json()
print(response)
