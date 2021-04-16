from os import listdir
from os.path import isfile, join
from matches import Matches

class Players(Matches):
    def __init__(self,teams):
        self.teams=teams

    def matches_per_team(self,team):
        matches=[]
        for match in (self.get_all_matches()):
            if team in match:
                matches.append(match)
        return matches

    def matches_per_all_teams(self):
        matches={}
        for team in self.teams:
            team_match=[]
            for match in (self.get_all_matches()):
                if team in match:
                    team_match.append(match)
            matches[team]=team_match
        return matches

teams = [f for f in listdir("../resources/teams") if isfile(join("../resources/teams", f))]
P1 = Players(teams)
print(P1.matches_per_all_teams())
