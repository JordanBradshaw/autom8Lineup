import argparse
import datetime
import json

import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2

# today = datetime.date.today()
# print(today)
# prev = datetime.date(2021, 1, 18)
# print(prev)


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


class leagueManager:
    def __init__(self, passedLeague):
        self.currentLeague = passedLeague

    def getCurrentWeek(self):
        # currentLeague.
        # nonlocal currentLeague
        print(self.currentLeague.matchups())

    #    pass


def cli():
    # Setup up connection to yahoo and select NBA
    oauth = connectionManager()
    sport = yfa.Game(oauth, "nba")

    def chooseLeague(possibleChoices):
        print("Choose from the following League IDs:")
        print("----------------------------------")
        for index, league in enumerate(possibleLeagues):
            print(f"Index: {index} League ID: {league}")
        print("----------------------------------")
        while True:
            returnLeague = input("Input the index you're selecting or type -1 to exit: ")
            try:
                if returnLeague == "-1":
                    print("Exiting...")
                    exit()
                elif int(returnLeague) > -1 and int(returnLeague) <= possibleChoices:
                    return int(returnLeague)
                    break
                else:
                    print("-Error: Invalid Index!-")
            except ValueError:
                print("-Error: Invalid Input!-")

    possibleLeagues = sport.league_ids(year=2020)
    leagueIndex = chooseLeague(len(possibleLeagues) - 1)
    currentLeague = sport.to_league(possibleLeagues[leagueIndex])
    temp = leagueManager(currentLeague)
    # print(currentLeague.matchups())
    for agent in currentLeague.free_agents("PF"):
        print(agent)
    return
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
