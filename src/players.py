from os import listdir
from os.path import isfile, join
from matches import Matches

class Players(Matches):
    def __init__(self,teams):
        self.teams=teams

    def matches_per_team(self,team):
        for match in (P1.get_all_matches()):
            print(match)
            if match.find(team) == 0:



teams = [f for f in listdir("../resources/teams") if isfile(join("../resources/teams", f))]
P1 = Players(teams)
P1.matches_per_team("csk")
