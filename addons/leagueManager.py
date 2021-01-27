import argparse
import datetime

# from inquirer Successfully installed Pygments-2.7.4 prompt-toolkit-1.0.14 pyinquirer-1.0.3 regex-2020.11.13 six-1.15.0 wcwidth-0.2.5

# today = datetime.date.today()
# print(today)
# prev = datetime.date(2021, 1, 18)
# print(prev)


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
        return currentRoster

    def getWeeksMatchup(self):
        currentMatchup = self.currentLeague.matchups()
        #currentDay = datetime.date(2021, 1, 22)
        # teamVariable = self.currentLeague.to_team(
        #    self.currentLeague.team_key())
        #currentMatchup = teamVariable.roster(currentWeek, currentDay)
        return currentMatchup

    def getTopFreeAgents(self):
        returnDict = {}
        positions = ['PG', 'SG', 'SF', 'PF', 'C']
        for item in positions:
            returnDict[item] = sorted(self.currentLeague.free_agents(
                item), key=lambda i: i['percent_owned'], reverse=True)[:5]
        # currentLeague.
        # nonlocal currentLeague
        return returnDict

    def getCategories(self):
        for item in self.currentLeague.stat_categories():
            print(item)
