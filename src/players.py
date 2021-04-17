from os import listdir
from os.path import isfile, join
from teams import Teams
from files import readFile, writeFile, appendFile
import json

class Players(Teams):
    def __init__(self,teams):
        super().__init__(teams)

    def get_stats(self):
        player_stats={}

        for teams in self.get_teams():
            team=readFile("../resources/teams/"+teams)
            match_stat={}
            for match in team:
                for innings in team[match]:
                    for inning in innings:
                        for player in inning:
                            if isinstance(player,dict):
                                player_name=player["name"]
                                stat={}
                                if 'wickets' in player:
                                    stat["bowling_stat"]=player
                                if 'runs' in player:
                                    stat["batting_stat"]=player
                        match_stat[match]=stat
                player_stats[player_name]=match_stat
        print(player_stats)

teams = [f for f in listdir("../resources/teams") if isfile(join("../resources/teams", f))]
P1=Players(teams)
P1.get_stats()
