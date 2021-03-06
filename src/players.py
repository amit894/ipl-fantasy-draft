from os import listdir
from os.path import isfile, join
from teams import Teams
from files import readFile, writeFile, appendFile
import json
import asyncio
import csv

class Players(Teams):
    def __init__(self,teams):
        super().__init__(teams)

    def get_stats(self):
        player_stats=[]
        player_list=[]
        players={"test_player"}

        for teams in self.get_teams():
            team=readFile("../resources/scores/team_scores/"+teams)
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
                                        print(stat)
                                if len(player)==2:
                                    #print(list(player.keys())[0],list(player.values())[0])
                                    for key in player:
                                        if key in "playing":
                                            pass
                                        else:
                                            #print(key+"_"+str(match)+"_playing_stat")
                                            stat[key+"_"+teams.split(".")[0]+"_"+str(match)+"_playing_stat"]=player[key]
                                            player_stats.append(stat)
                                            players.add(key+"_"+teams.split(".")[0])

        player_list.append(players)
        player_list.append(player_stats)
        return player_list


    def update_player_stats(self,players,player_stats):
        masterlist=readFile("../resources/players.json")
        updated_player_stats={}
        sorted_players=list(players)
        sorted_players.sort()
        for key1 in sorted_players:
            l1=[]
            for key2 in player_stats:
                for key3 in key2:
                    temp_dict={}
                    key4=masterlist[key3.split("_")[0]]
                    if(key1.split("_")[0].find(key4)>=0):
                        temp_dict[key3.split("_")[2]+"_"+key3.split("_")[3]]=key2[key3]
                        l1.append(temp_dict)
            updated_player_stats[key1]=l1
        #print(len(updated_player_stats))
        #print("De delimiters")
        return(updated_player_stats)

    def remove_duplicate_elements(self,list1):
        masterlist={}
        masterlist=readFile("../resources/players.json")
        temp_list=set()
        for player in list1:
            #print(masterlist[player.split("_")[0]])
            #print(masterlist[player.split("_")[0]]+'_'+player.split("_")[1])
            temp_list.add(masterlist[player.split("_")[0].strip()]+'_'+player.split("_")[1].strip())
        print(len(list1),len(temp_list))
        list1=list(temp_list)
        return(list1)



    def update_stats(self,updated_player_stats):
        overall_stats=updated_player_stats
        for players in updated_player_stats:
            #print(overall_stats[players])
            writeFile("../resources/scores/player_scores/"+players.split('_')[1]+"/"+players.split('_')[0],overall_stats[players])

    #
    def update_batting_points(self,batting_info):
        batting_points=0
        milestone_points=0
        sr_points=0
        if int(batting_info['runs'])>=200:
            milestone_points=100
        elif int(batting_info['runs'])>150:
            milestone_points=80
        elif int(batting_info['runs'])>=100:
            milestone_points=50
        elif int(batting_info['runs'])>=50:
            milestone_points=20


        if int(batting_info['balls'])>=10:
            if float(batting_info['sr'])<50:
                sr_points=-20
            elif float(batting_info['sr'])<75:
                sr_points=-10
            elif float(batting_info['sr'])<100:
                sr_points=-5
            elif float(batting_info['sr'])<150:
                sr_points=10
            elif float(batting_info['sr'])<200:
                sr_points=15
            elif float(batting_info['sr'])>=200:
                sr_points=20

        batting_points=int(batting_info['runs'])+int(batting_info['fours'])+int(batting_info['sixes'])*2
        total_points=batting_points+sr_points+milestone_points

        return total_points

    def update_bowling_points(self,bowling_info):
        bowling_points=0
        milestone_points=0
        ec_points=0

        if int(bowling_info['wickets'])>=5:
            milestone_points=50
        elif int(bowling_info['wickets'])>=4:
            milestone_points=40
        elif int(bowling_info['wickets'])>=3:
            milestone_points=25

        if int(float(bowling_info['overs']))>=2:
            if float(bowling_info['ec'])>12:
                ec_points=-20
            elif float(bowling_info['ec'])>10:
                ec_points=-10
            elif float(bowling_info['ec'])>7:
                ec_points=0
            elif float(bowling_info['ec'])>5:
                ec_points=10
            elif float(bowling_info['ec'])<=5:
                ec_points=20

        bowling_points=int(bowling_info['wickets'])*25+int(bowling_info['maiden'])*10
        total_points=bowling_points+ec_points+milestone_points

        return total_points


    def update_fielding_points(self,fielding_info):
        return (fielding_info*10)

    def update_playing_points(self,playing_info):
        return (playing_info*5)



    def update_points(self):
        for team in self.get_teams():
            players = [f for f in listdir("../resources/scores/player_scores/"+team.split('.')[0]) if isfile(join("../resources/scores/player_scores/"+team.split('.')[0], f))]
            raw_data={}
            for player in players:
                temp_player_dict={}
                raw_data=readFile("../resources/scores/player_scores/"+team.split('.')[0]+"/"+player)
                for key in raw_data:
                    for key1 in key:
                        temp_list=key1.split('_')
                        if(temp_list[1]=="batting"):
                            temp_batting_points=self.update_batting_points(key[key1])
                            temp_player_dict[temp_list[0]+"_batting_points"]=temp_batting_points
                        if(temp_list[1]=="bowling"):
                            temp_bowling_points=self.update_bowling_points(key[key1])
                            temp_player_dict[temp_list[0]+"_bowling_points"]=temp_bowling_points
                        if(temp_list[1]=="fielding"):
                            temp_fielding_points=self.update_fielding_points(key[key1])
                            temp_player_dict[temp_list[0]+"_fielding_points"]=temp_fielding_points
                        if(temp_list[1]=="playing"):
                            temp_playing_points=self.update_playing_points(key[key1])
                            temp_player_dict[temp_list[0]+"_playing_points"]=temp_playing_points
                #print(player,temp_player_dict)
                writeFile("../resources/points/players/"+player, temp_player_dict)


teams = [f for f in listdir("../resources/scores/team_scores") if isfile(join("../resources/scores/team_scores", f))]
P1=Players(teams)
main_player_stats=P1.get_stats()
main_player_stats[0]=P1.remove_duplicate_elements(main_player_stats[0])
updated_player_stats=P1.update_player_stats(main_player_stats[0],main_player_stats[1])
P1.update_stats(updated_player_stats)
P1.update_points()
