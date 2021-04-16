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
        except:
            return ("Error reading from file")


O1=Owners("ahuja",1)
print(O1.readPlayers())
