from os import listdir
from os.path import isfile, join
from teams import Teams
from files import readFile, writeFile, appendFile
import json

class Players(Teams):
    def __init__(self,teams):
        super().__init__(teams)

    def get_stats(self):
        self.player_stats={}

        for teams in self.get_teams():
            team=readFile("../resources/teams/"+teams)
            for match in team:
                for innings in team[match]:
                    for inning in innings:
                        for player in inning:
                            match_stat={}
                            player_name=''
                            stat={}
                            if isinstance(player,dict):
                                player_name=player["name"]+"_"+teams.split(".")[0]
                                if 'wickets' in player:
                                    stat["bowling_stat"]=player
                                if 'runs' in player:
                                    stat["batting_stat"]=player
                            else:
                                for x in inning:
                                    player_name=x+"_"+teams.split(".")[0]
                                    stat["fielding_stat"]=inning[x]
                            match_stat[match]=stat
                            self.player_stats[player_name]=match_stat
        print(self.player_stats)

    def update_stats(self):
        print(self.get_teams())

teams = [f for f in listdir("../resources/teams") if isfile(join("../resources/teams", f))]
P1=Players(teams)
P1.get_stats()
