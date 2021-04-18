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


owners=["ahuja","bapu","supan","shreyans","dusty","pranky","bha1"]

for i in range(len(owners)):
    owner_sum=0
    temp_dict={}
    O1=Owners(owners[i],i)
    players=O1.readPlayers()
    for player in players:
        #print(player['player'])
        json_data=readFile("../resources/points/players/"+player['player'])
        if ("Error" in json_data):
            owner_sum+=0
        else:
            player_sum=0
            for data in json_data:
                #print(json_data[data])
                player_sum+=int(json_data[data])
            owner_sum+=player_sum
    print(owner_sum)
    temp_dict[owners[i]]=owner_sum
    appendFile("../resources/points/owners/points.json", temp_dict)
