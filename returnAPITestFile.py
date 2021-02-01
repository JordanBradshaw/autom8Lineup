# import mypackage.modules.addons.getLeagueCLI
import yahoo_fantasy_api as yfa
from modules import getLeagueCLI

# from . import addons.getLeagueCLI

# from autom8Lineup.addons import getLeagueCLI


# from ..addons import connectionManager, getLeagueCLI, leagueManager


def testing():
    testingVar = getLeagueCLI.getLeague()
    print(testingVar.getCategories())


testing()
