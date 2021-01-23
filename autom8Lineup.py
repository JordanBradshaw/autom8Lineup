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
        credentials = {
            'consumer_key':
            'dj0yJmk9b0JiZHhhMmROb2FOJmQ9WVdrOWVFZFVVR0pRWmxZbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTMz',
            'consumer_secret': '3156308ff948c61ac5078f7f143c81555df75339',
        }
        with open('oauth2.json', 'w') as f:
            f.write(json.dumps(credentials))
        return OAuth2(None, None, from_file='oauth2.json')

    def checkValidOrRefreshToken():
        return OAuth2(None, None, from_file='oauth2.json')

    try:  ##Check if oauth2 file exists if it does open oauth with the file
        fileExistCheck = open('oauth2.json')
        return checkValidOrRefreshToken()
    except IOError:  # if file does not exist run connection manager and create a token
        return noToken()


class leagueManager:
    def __init__(self, passedLeague):
        self.currentLeague = passedLeague

    def getLeagueSettings(self):
        print(self.currentLeague.settings())

    def getCurrentWeek(self):
        print(self.currentLeague.matchups())

    def getTodaysRoster(self):
        currentWeek = self.currentLeague.current_week()
        currentDay = datetime.date(2021, 1, 22)
        teamVariable = self.currentLeague.to_team(
            self.currentLeague.team_key())
        currentRoster = teamVariable.roster(currentWeek, currentDay)
        print('------------- CURRENT ROSTER -------------')
        for item in currentRoster:
            print(item)

    def getTopFreeAgents(self):
        # currentLeague.
        # nonlocal currentLeague
        print(self.currentLeague.matchups())

    def getCategories(self):
        for item in self.currentLeague.stat_categories():
            print(item)

    #    pass


def cli():
    def getLeagueName(passedLeagueValue):
        return yfa.League(oauth, passedLeagueValue).settings()['name']

    # Setup up connection to yahoo and select NBA
    oauth = connectionManager()
    sport = yfa.Game(oauth, 'nba')

    def chooseLeague(possibleChoices):
        print('Choose from the following League IDs:')
        print('----------------------------------')
        for index, league in enumerate(possibleLeagues):
            leagueName = getLeagueName(league)
            print(
                f'Index: {index} League Name: {leagueName} League ID: {league}'
            )
        print('----------------------------------')
        while True:
            returnLeague = input(
                "Input the index you're selecting or type -1 to exit: ")
            try:
                if returnLeague == '-1':
                    print('Exiting...')
                    exit()
                elif int(returnLeague) > -1 and int(
                        returnLeague) <= possibleChoices:
                    return int(returnLeague)
                    break
                else:
                    print('-Error: Invalid Index!-')
            except ValueError:
                print('-Error: Invalid Input!-')

    possibleLeagues = sport.league_ids(year=2020)
    leagueIndex = chooseLeague(len(possibleLeagues) - 1)
    currentLeague = sport.to_league(possibleLeagues[leagueIndex])
    temp = leagueManager(currentLeague)
    # print(currentLeague.matchups())
    temp.getTodaysRoster()
    temp.getCategories()
    return

    currentRoster = currentLeague.to_team(currentTeam)
    # print(currentRoster.roster(1))
    for item in currentRoster.roster(day=prev):
        print(item)


if __name__ == '__main__':
    cli()
