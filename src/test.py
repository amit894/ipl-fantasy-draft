import csv
import json
from files import readFile, writeFile, appendFile

f1 = open("../resources/owners/shreyans.csv")
f2 = open("../resources/owners/shreyans.json","w")
list=[]
i=0
csv_reader= csv.reader(f1, delimiter=',')
for row in csv_reader:
    test={}
    x=row[0].split()
    y=x[0]+x[1]
    test['player']=y
    test['team']=x[2]
    test['id']=i
    i=i+1
    #print(test)
    list.append(test)
print(list)
json.dump(list,f2)
f2.close()
f1.close()
