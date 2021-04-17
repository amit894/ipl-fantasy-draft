from os import listdir
from os.path import isfile, join
from teams import Teams
from files import readFile, writeFile, appendFile
import json
import asyncio

class Players(Teams):
    def __init__(self,teams):
        super().__init__(teams)

    async def get_stats(self):
        self.player_stats={}

        for teams in self.get_teams():
            team=readFile("../resources/team_scores/"+teams)
            for match in team:
                for innings in team[match]:
                    for inning in innings:
                        for player in inning:
                            if isinstance(player,dict):
                                player_name=[]
                                match_stat={}
                                stat={}
                                player_name.append(player["name"]+"_"+teams.split(".")[0])
                                if 'wickets' in player:
                                    stat["bowling_stat"]=player
                                if 'runs' in player:
                                    if 'sr' in player:
                                        stat["batting_stat"]=player
                                match_stat[match]=stat
                                print(player_name[0])
                                self.player_stats[player_name[0]]=match_stat
                            else:
                                for x in inning:
                                    player_name=[]
                                    match_stat={}
                                    stat={}
                                    player_name.append(x+"_"+teams.split(".")[0])
                                    stat["fielding_stat"]=inning[x]
                                    match_stat[match]=stat
                                    print(player_name[0])
                                    self.player_stats[player_name[0]]=match_stat
        #print(self.player_stats)
        return self.player_stats

    async def update_stats(self):
        overall_stats=self.player_stats
        for players in overall_stats:
            #print(players)
            #print("delimiters")
            writeFile("../resources/player_scores/"+players.split('_')[1]+"/"+players.split('_')[0],overall_stats[players])


async def main():
    teams = [f for f in listdir("../resources/team_scores") if isfile(join("../resources/team_scores", f))]
    P1=Players(teams)
    await P1.get_stats()
    await P1.update_stats()

asyncio.run(main())
