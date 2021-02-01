import curses
import json
import time
from typing import List

import pandas as pd
import requests
import yahoo_fantasy_api as yfa

from modules import connectionManager, leagueManager

menu = ["Roster", "Matchup", "Players", "League"]


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
        stdscr.addstr(3 + h, x, player["selected_position"])
        x = ((w // 4) * 2) - (len(player["name"]) // 2)
        stdscr.addstr(3 + h, x, player["name"])

    printMenu(stdscr, ["", menu[0], menu[1]], h, w)
    todaysRoster = globalLeague.getTodaysRoster()
    print(todaysRoster)
    for index, player in enumerate(todaysRoster):
        formatRoster(stdscr, player, index, w)

    stdscr.refresh()


# Hello


def printMatchup(stdscr, h, w):
    def formatMatchup(stdscr, player, h, w):
        x = (w // 10) * 3
        stdscr.addstr(3 + h, x, player["selected_position"])
        x = ((w // 4) * 2) - (len(player["name"]) // 2)
        stdscr.addstr(3 + h, x, player["name"])

    printMenu(stdscr, [menu[0], menu[1], menu[2]], h, w)
    todaysMatchup = globalLeague.getWeeksMatchup()
    stdscr.refresh()


def printPlayers(stdscr, h, w):
    def formatPlayers(stdscr, h, w, key, items):
        positions = ["PG", "SG", "SF", "PF", "C"]
        x = ((w // 6) * (positions.index(key) + 1)) - (len(key) // 2)
        stdscr.addstr(3, x, key)
        for index, item in enumerate(items, start=4):
            x = ((w // 6) * (positions.index(key) + 1)) - (len(item["name"]) // 2)
            stdscr.addstr(index, x, item["name"])

    printMenu(stdscr, [menu[1], menu[2], menu[3]], h, w)
    topFAs = globalLeague.getTopFreeAgents()
    for key, item in topFAs.items():
        formatPlayers(stdscr, h, w, key, item)
    stdscr.refresh()


def printLeague(stdscr, h, w):
    def formatMatchup(stdscr, player, h, w):
        x = (w // 10) * 3
        stdscr.addstr(3 + h, x, player["selected_position"])
        x = ((w // 4) * 2) - (len(player["name"]) // 2)
        stdscr.addstr(3 + h, x, player["name"])

    printMenu(stdscr, [menu[2], menu[3], ""], h, w)
    todaysMatchup = globalLeague.getWeeksMatchup()
    # print(todaysMatchup)
    # for index, player in enumerate(todaysRoster):
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
        # printMenu(stdscr, selectedColumnIndex)
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
    if selectedColumnIndex == 2:
        printPlayers(stdscr, h, w)
    if selectedColumnIndex == 3:
        printLeague(stdscr, h, w)


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
            returnLeague = input(
                "Input the index you're selecting or type -1 to exit: "
            )
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
    roster = leagueManager.leagueManager(currentLeague).getTodaysRoster()
    matchups = leagueManager.leagueManager(currentLeague).getWeeksMatchup()
    player_id = leagueManager.leagueManager(currentLeague).getPlayerIds()
    x = leagueManager.leagueManager(currentLeague).getPlayerStats(player_id)
    # for playerId in roster:
    #     for key in playerId:
    #         print("{}: {}".format(key, playerId[key]))
    for v, k in x.items():
        print(v, k)

    # print(x)
    # print(roster)
    # for item in stats:
    #     print(stats)
    exit()
    # for item in roster(
    #         matchups['fantasy_content']['league'][1]['scoreboard']['0']
    #     ['matchups']['0']['matchup']['status']):
    #     print(item)
    #     print(' ')

    # print(roster)
    # print(matchups)
    for index, item in enumerate(
        matchups["fantasy_content"]["league"][1]["scoreboard"]["0"]["matchups"]["0"][
            "matchup"
        ]["status"]
    ):
        print(index, item)
        print(" ")

    # for item, key in pgs.items():
    #    print(key)
    # print(pgs)
    # exit()
    return leagueManager.leagueManager(currentLeague)
    # print(currentLeague.matchups())
    temp.getTodaysRoster()
    time.sleep(10)

    return


globalLeague = getLeague()
curses.wrapper(commandLineInterface)
# if __name__ == "__main__":
#    cli()
