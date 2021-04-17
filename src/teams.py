from os import listdir
from os.path import isfile, join
from matches import Matches
from files import readFile, writeFile, appendFile
import asyncio



class Teams(Matches):
    def __init__(self,teams):
        self.team_names=teams

    async def update_matches_per_teams(self):
        self.overall_matches={}
        for team in self.team_names:
            team_match=[]
            for match in self.get_all_matches():
                if (match.find(team.split('.')[0])>=0):
                    team_match.append(match)
            self.overall_matches[team]=team_match
        return self.overall_matches

    async def get_teams(self):
        return(self.team_names)

    async def update_stats_all_teams(self):
        for key in self.overall_matches:
            if (key=="dc.json"):
                overall_team_data={}
                for match_file in self.overall_matches[key]:
                    match_data=readFile("../resources/matches/"+match_file)
                    for key1 in match_data:
                        team_data=[]
                        if ((key.split('.')[0])==(key1.split('_')[0])):
                            team_data.append(match_data[key1])
                            print(team_data)
                        overall_team_data[match_file.split('-')[0]]=team_data
                    #writeFile("../resources/teams/"+key, overall_team_data)

async def main():
    teams = [f for f in listdir("../resources/teams") if isfile(join("../resources/teams", f))]
    T1 = Teams(teams)
    await T1.update_matches_per_teams()
    await T1.update_stats_all_teams()

asyncio.run(main())
