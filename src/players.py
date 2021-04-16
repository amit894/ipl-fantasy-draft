from os import listdir
from os.path import isfile, join
from matches import Matches

class Players(Matches):
    def __init__(self,teams):
        self.teams=teams

    def get_matches_per_teams(self):
        self.overall_matches={}
        for team in self.teams:
            team_match=[]
            for match in self.get_all_matches():
                if (match.find(team.split('.')[0])>=0):
                    team_match.append(match)
            self.overall_matches[team]=team_match
        return self.overall_matches

    def get_stats_all_teams(self):
        for key in self.overall_matches:
            print(self.overall_matches[key])

teams = [f for f in listdir("../resources/teams") if isfile(join("../resources/teams", f))]
P1 = Players(teams)
P1.get_matches_per_teams()
P1.get_stats_all_teams()
