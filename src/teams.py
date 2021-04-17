from os import listdir
from os.path import isfile, join
from matches import Matches
from files import readFile, writeFile, appendFile


class Teams(Matches):
    def __init__(self,teams):
        self.team_names=teams

    def update_matches_per_teams(self):
        self.overall_matches={}
        for team in self.team_names:
            team_match=[]
            for match in self.get_all_matches():
                if (match.find(team.split('.')[0])>=0):
                    team_match.append(match)
            self.overall_matches[team]=team_match
        return self.overall_matches

    def get_teams(self):
        return(self.team_names)

    def update_stats_all_teams(self):
        for key in self.overall_matches:
            overall_team_data={}
            for match_file in self.overall_matches[key]:
                match_data=readFile("../resources/matches/"+match_file)
                team_data=[]
                for key1 in match_data:
                    if (key1.find(key.split('.')[0])>=0):
                        team_data.append(match_data[key1])
                overall_team_data[match_file.split('-')[0]]=team_data
            writeFile("../resources/teams/"+key, overall_team_data)

teams = [f for f in listdir("../resources/teams") if isfile(join("../resources/teams", f))]
T1 = Teams(teams)
T1.update_matches_per_teams()
T1.update_stats_all_teams()
