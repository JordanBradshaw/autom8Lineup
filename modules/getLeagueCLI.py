import yahoo_fantasy_api as yfa

from . import connectionManager, leagueManager


def getLeague():
    def getLeagueName(passedLeagueValue):
        return yfa.League(oauth, passedLeagueValue).settings()["name"]

    # Setup up connection to yahoo and select NBA
    oauth = connectionManager.connectionManager()
    sport = yfa.Game(oauth, "nba")

    def chooseLeague(possibleChoices):
        print("Choose from the following League IDs:")
        print("----------------------------------")
        for index, league in enumerate(possibleLeagues):
            leagueName = getLeagueName(league)
            print(f"Index: {index} League Name: {leagueName} League ID: {league}")
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
    lM = leagueManager.leagueManager(currentLeague)
    return lM
