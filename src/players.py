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
        player_list=[]
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
                                if 'wickets' in player:
                                    player_name.append(player["name"]+"_"+teams.split(".")[0])
                                    stat[player_name[0]+"_"+str(match)+"_bowling_stat"]=player
                                    player_stats.append(stat)
                                    players.add(player_name[0])
                                if 'runs' in player:
                                    if 'sr' in player:
                                        player_name.append(player["name"]+"_"+teams.split(".")[0])
                                        stat[player_name[0]+"_"+str(match)+"_batting_stat"]=player
                                        player_stats.append(stat)
                                        players.add(player_name[0])
                                if len(player)==1:
                                    for key in player:
                                        player_name.append(key+"_"+teams.split(".")[0])
                                        stat[player_name[0]+"_"+str(match)+"_fielding_stat"]=player[key]
                                        player_stats.append(stat)
                                        players.add(player_name[0])

        player_list.append(players)
        player_list.append(player_stats)
        return player_list


    async def update_player_stats(self,players,player_stats):
        updated_player_stats={}
        sorted_players=list(players)
        sorted_players.sort()
        for key1 in sorted_players:
            l1=[]
            for key2 in player_stats:
                for key3 in key2:
                    temp_dict={}
                    if(key1.split("_")[0].find(key3.split("_")[0])>=0):
                        temp_dict[key3.split("_")[2]+"_"+key3.split("_")[3]]=key2[key3]
                        l1.append(temp_dict)
            updated_player_stats[key1]=l1
        #print(len(updated_player_stats))
        #print("De delimiters")
        return(updated_player_stats)


    async def diff(self,li1,li2):
            return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

    async def twoStrings(s1, s2):
        v = [0] * (MAX_CHAR)
        for i in range(len(s1)):
            v[ord(s1[i]) - ord('a')] = True
        for i in range(len(s2)) :
            if (v[ord(s2[i]) - ord('a')]) :
                return True

        return False


    async def remove_duplicate_elements(self,list1):
        masterlist=readFile("../resources/players.json")
        temp_list=set()
        for player in list1:
            temp_list.add(masterlist[player.split("_")[0]]+'_'+player.split("_")[1])
        print(len(list1),len(temp_list))
        list1=list(temp_list)
        return(list1)



    async def update_stats(self,updated_player_stats):
        overall_stats=updated_player_stats
        for players in updated_player_stats:
            writeFile("../resources/player_scores/"+players.split('_')[1]+"/"+players.split('_')[0],overall_stats[players])


async def main():
    teams = [f for f in listdir("../resources/team_scores") if isfile(join("../resources/team_scores", f))]
    P1=Players(teams)
    main_player_stats=await P1.get_stats()
    main_player_stats[0]=await P1.remove_duplicate_elements(main_player_stats[0])
    # #print(main_player_stats[0])
    updated_player_stats=await P1.update_player_stats(main_player_stats[0],main_player_stats[1])
    await P1.update_stats(updated_player_stats)

asyncio.run(main())
