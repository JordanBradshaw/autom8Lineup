import argparse
import datetime
import json

import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2

# today = datetime.date.today()
# print(today)
prev = datetime.date(2021, 1, 18)
print(prev)


def connectionManager():
    def noToken():
        # ap = argparse.ArgumentParser()
        # args = vars(ap.parse_args())
        credentials = {
            "consumer_key": "dj0yJmk9b0JiZHhhMmROb2FOJmQ9WVdrOWVFZFVVR0pRWmxZbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTMz",
            "consumer_secret": "3156308ff948c61ac5078f7f143c81555df75339",
        }
        with open("oauth2.json", "w") as f:
            f.write(json.dumps(credentials))
        return OAuth2(None, None, from_file="oauth2.json")

    def checkValidOrRefreshToken():
        return OAuth2(None, None, from_file="oauth2.json")

    try:  ##Check if oauth2 file exists if it does open oauth with the file
        fileExistCheck = open("oauth2.json")
        return checkValidOrRefreshToken()
    except IOError:  # if file does not exist run connection manager and create a token
        return noToken()


# class leagueManager:


def cli():
    def chooseLeague():
        print("Choose from the following League IDs:")
        for index, league in enumerate(validLeague):
            print(f"Index: {index} League ID: {league}")
        return input("Input the index you're selecting or type -1 to exit: ")

    oauth = connectionManager()
    sport = yfa.Game(oauth, "nba")
    validLeague = sport.league_ids(year=2020)
    print(list(enumerate(validLeague)))
    possibleChoices = len(validLeague) - 1
    while True:
        returnLeague = chooseLeague()
        try:
            if returnLeague == "-1":
                print("Exiting...")
                exit()
            elif int(returnLeague) > -1 and int(returnLeague) <= possibleChoices:
                leagueIndex = int(returnLeague)
                break
            else:
                print("-Error: Invalid Index!-")
        except ValueError:
            print("-Error: Invalid Input!-")
    currentLeague = sport.to_league(validLeague[leagueIndex])

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


if __name__ == "__main__":
    cli()
