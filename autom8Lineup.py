import argparse
import datetime
import json

import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2

# today = datetime.date.today()
# print(today)
prev = datetime.date(2021, 1, 18)
print(prev)


def findCredentials(request):
    ap = argparse.ArgumentParser()
    args = vars(ap.parse_args())
    credit = {
        "consumer_key": "dj0yJmk9b0JiZHhhMmROb2FOJmQ9WVdrOWVFZFVVR0pRWmxZbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTMz",
        "consumer_secret": "3156308ff948c61ac5078f7f143c81555df75339",
    }
    with open("oauth2.json", "w") as f:
        f.write(json.dumps(credit))


def default():
    oauth = OAuth2(None, None, from_file="oauth2.json")

    gm = yfa.Game(oauth, "nba")
    validLeague = gm.league_ids(year=2020)
    print(validLeague)
    currentLeague = gm.to_league(validLeague[0])
    print(currentLeague.stat_categories())
    currentTeam = currentLeague.team_key()
    currentWeek = currentLeague.current_week()
    endWeek = currentLeague.end_week()
    print(currentWeek)
    print(endWeek)
    print("------------- CURRENT ROSTER -------------")
    currentRoster = currentLeague.to_team(currentTeam)
    # print(currentRoster.roster(1))
    for item in currentRoster.roster(day=prev):
        print(item)


default()
