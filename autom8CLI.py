import curses
import time

import yahoo_fantasy_api as yfa

from addons import connectionManager, leagueManager

menu = ['Roster', 'Matchup', 'Players', 'League']


def printMenu(stdscr, selectedColumnIndex):
    h, w = stdscr.getmaxyx()
    for index, word in enumerate(menu):
        x = ((w // (len(menu) + 1)) * (index + 1)) - (len(word) // 2)
        if index == selectedColumnIndex:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(1, x, word)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(1, x, word)


def printRoster(stdscr):
    h, w = stdscr.getmaxyx()
    todaysRoster = globalLeague.getTodaysRoster()
    print(todaysRoster)
    for item in enumerate(todaysRoster):
        print(item)
        #x = ((w // (len(menu) + 1)) * (index + 1)) - (len(word) // 2)

        #stdscr.addstr(1, x, word)


def commandLineInterface(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    selectedColumnIndex = 0
    printMenu(stdscr, selectedColumnIndex)
    time.sleep(1)
    while 1:
        key = stdscr.getch()
        stdscr.clear()
        #printMenu(stdscr, selectedColumnIndex)
        if key == curses.KEY_LEFT and selectedColumnIndex > 0:
            selectedColumnIndex -= 1
        elif key == curses.KEY_RIGHT and selectedColumnIndex < len(menu) - 1:
            selectedColumnIndex += 1
        activeMenu(stdscr, selectedColumnIndex)
        printMenu(stdscr, selectedColumnIndex)
        #time.sleep(10000)
        stdscr.refresh()


def activeMenu(stdscr, selectedColumnIndex):
    if selectedColumnIndex == 0:
        printRoster(stdscr)


def getLeague():
    def getLeagueName(passedLeagueValue):
        return yfa.League(oauth, passedLeagueValue).settings()['name']

    # Setup up connection to yahoo and select NBA
    oauth = connectionManager.connectionManager()
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
    roster = leagueManager.leagueManager(currentLeague).getTodaysRoster()
    #print(roster['name']
    return leagueManager.leagueManager(currentLeague)
    # print(currentLeague.matchups())
    temp.getTodaysRoster()
    time.sleep(10)

    return


globalLeague = getLeague()
curses.wrapper(commandLineInterface)
#if __name__ == "__main__":
#    cli()
