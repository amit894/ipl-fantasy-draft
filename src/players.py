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
        player_stats=[]
        temp_list=[]
        players={"test_player"}

        for teams in self.get_teams():
            team=readFile("../resources/team_scores/"+teams)
            for match in team:
                for innings in team[match]:
                    for inning in innings:
                        for player in inning:
                            if isinstance(player,dict):
                                player_name=[]
                                stat={}
                                player_name.append(player["name"]+"_"+teams.split(".")[0])
                                if 'wickets' in player:
                                    stat[player_name[0]+"_"+str(match)+"_bowling_stat"]=player
                                if 'runs' in player:
                                    if 'sr' in player:
                                        stat[player_name[0]+"_"+str(match)+"_batting_stat"]=player

                                player_stats.append(stat)
                                players.add(player_name[0])
                            else:
                                for x in inning:
                                    player_name=[]
                                    stat={}
                                    player_name.append(x+"_"+teams.split(".")[0])
                                    stat[player_name[0]+"_"+str(match)+"_fielding_stat"]=inning[x]
                                    player_stats.append(stat)
                                    players.add(player_name[0])

        temp_list.append(players)
        temp_list.append(player_stats)
        return temp_list


    async def update_player_stats(self,players,player_stats):
        updated_player_stats={}
        sorted_players=list(players)
        sorted_players.sort()
        #print(sorted_players))
        for key1 in sorted_players:
            l1=[]
            for key2 in player_stats:
                for key3 in key2:
                    temp_dict={}
                    if(key1.split("_")[0].find(key3.split("_")[0])==0):
                        temp_dict[key3.split("_")[2]+"_"+key3.split("_")[3]]=key2[key3]
                        l1.append(temp_dict)
            updated_player_stats[key1]=l1
        #print(len(updated_player_stats))
        #print("De delimiters")
        return(updated_player_stats)


    # async def update_players(self):
    #     #temp_players={"Rajat Patidar_rcb":0, "Patidar_rcb":0, "Amit Raj":0, "Raj":0}
    #
    #     temp_players={}
    #     for player in self.players:
    #         temp_players[player]=0
    #
    #
    #     for key1 in temp_players:
    #         for key2 in temp_players:
    #             if(key2.find(key1)>0 and temp_players[key2]==0):
    #                 temp_players[key2]=1
    #     #print(temp_players)
    #
    #     l1=[]
    #     l2=[]
    #
    #     for key in temp_players:
    #        if (temp_players[key]==0):
    #            l1.append(key)
    #        else:
    #            l2.append(key)
    #
    #     print(len(l1),len(l2),len(temp_players))

    async def update_stats(self,updated_player_stats):
        overall_stats=updated_player_stats
        print(len(updated_player_stats))
        for players in updated_player_stats:
            print(updated_player_stats[players])
            print("delimiters")
            writeFile("../resources/player_scores/"+players.split('_')[1]+"/"+players.split('_')[0],overall_stats[players])


async def main():
    teams = [f for f in listdir("../resources/team_scores") if isfile(join("../resources/team_scores", f))]
    P1=Players(teams)
    player_stats=await P1.get_stats()
    updated_player_stats=await P1.update_player_stats(player_stats[0],player_stats[1])
    await P1.update_stats(updated_player_stats)

asyncio.run(main())
