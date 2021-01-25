import curses
import time
from typing import List

import yahoo_fantasy_api as yfa

from addons import connectionManager, leagueManager

menu = ['Roster', 'Matchup', 'Players', 'League']


def printMenu(stdscr, menuWords: List[str], h, w):
    for index, word in enumerate(menuWords, start=1):
        x = ((w // 4) * (index)) - (len(word) // 2)
        if index == 2:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(1, x, word)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(1, x, word)


def printRoster(stdscr, h, w):
    def formatRoster(stdscr, player, h, w):
        x = (w // 10) * 3
        stdscr.addstr(3 + h, x, player['selected_position'])
        x = ((w // 4) * 2) - (len(player['name']) // 2)
        stdscr.addstr(3 + h, x, player['name'])

    printMenu(stdscr, ["", menu[0], menu[1]], h, w)
    todaysRoster = globalLeague.getTodaysRoster()
    print(todaysRoster)
    for index, player in enumerate(todaysRoster):
        formatRoster(stdscr, player, index, w)

    stdscr.refresh()


def printMatchup(stdscr, h, w):
    def formatMatchup(stdscr, player, h, w):
        x = (w // 10) * 3
        stdscr.addstr(3 + h, x, player['selected_position'])
        x = ((w // 4) * 2) - (len(player['name']) // 2)
        stdscr.addstr(3 + h, x, player['name'])

    printMenu(stdscr, [menu[0], menu[1], menu[2]], h, w)
    todaysMatchup = globalLeague.getWeeksMatchup()
    #print(todaysMatchup)
    #for index, player in enumerate(todaysRoster):
    #    formatMatchup(stdscr, player, index, w)
    #
    stdscr.refresh()


def commandLineInterface(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    selectedColumnIndex = 0
    h, w = stdscr.getmaxyx()
    activeMenu(stdscr, selectedColumnIndex)
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
        stdscr.refresh()


def activeMenu(stdscr, selectedColumnIndex):
    h, w = stdscr.getmaxyx()
    if selectedColumnIndex == 0:
        printRoster(stdscr, h, w)
    if selectedColumnIndex == 1:
        printMatchup(stdscr, h, w)


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
    matchups = leagueManager.leagueManager(currentLeague).getWeeksMatchup()
    #print(roster)
    #print(matchups)
    for index, item in enumerate(
            matchups['fantasy_content']['league'][1]['scoreboard']['0']
        ['matchups']['0']['matchup']['status']):
        print(index, item)
        print(' ')

    #exit()
    return leagueManager.leagueManager(currentLeague)
    # print(currentLeague.matchups())
    temp.getTodaysRoster()
    time.sleep(10)

    return


globalLeague = getLeague()
curses.wrapper(commandLineInterface)
#if __name__ == "__main__":
#    cli()
