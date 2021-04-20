import json
from files import readFile, writeFile, appendFile


class Owners():
    def __init__(self,name,id):
        self.name=name
        self.id=id

    def readPlayers(self):
        try:
            f1=open('../resources/owners/'+self.name+'.json','r')
            players=json.load(f1)
            f1.close()
            return players
        except Exception as e:
            print(e)
            return ("Error reading from file")

    def sum11(self,list):
        sum=0
        for i in range(11):
            sum+=list[i]
        return sum


owners=["ahuja","bapu","supan","shreyans","dusty","pranky","bha1"]

temp_dict={}
for i in range(len(owners)):
    owner_sum=0
    O1=Owners(owners[i],i)
    players=O1.readPlayers()
    player_list=[]
    player_sum=0
    for player in players:
        #print(player['player'])
        innings_sum=0
        json_data=readFile("../resources/points/players/"+player['player'])
        if ("Error" in json_data):
            owner_sum+=0
        else:
            for data in json_data:
                innings_sum+=int(json_data[data])
            player_sum+=innings_sum
        player_list.append(innings_sum)
        player_list.sort(reverse=True)
    owner_sum=O1.sum11(player_list)
    #print(player_list)
    print(player_list)
    temp_dict[owners[i]]=owner_sum
    #print(owner_sum)
appendFile("../resources/points/owners/points.json", temp_dict)
