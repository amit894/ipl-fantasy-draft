from files import readFile, writeFile, appendFile
from scrapper import get_match
from os import listdir
from os.path import isfile, join

class Matches():
    def __init__(self,urls):
        self.urls=urls

    def update_match_score(self):
        for url in self.urls:
            match_id=''
            data=[]
            teams=[]
            if url["completed"]=="No":
                match_id=url["url"].split("/")[4]
                teams.append((url["url"].split("/")[5]).split("-")[0])
                teams.append((url["url"].split("/")[5]).split("-")[2])
                match_data=get_match(url["url"],teams)
                status=writeFile("../resources/matches/"+match_id+"-"+teams[0]+"-"+teams[1]+".json",match_data)
                if status=="Successful":
                    url_statuses=readFile("../resources/url.json")
                    for url_status in url_statuses:
                        if url_status['id']==url['id']:
                            url_status['completed']="Yes"
                    writeFile("../resources/url.json",url_statuses)

    def get_all_matches(self):
        matches = [f for f in listdir("../resources/matches") if isfile(join("../resources/matches", f))]
        return matches




urls=readFile("../resources/url.json")
M1=Matches(urls)
M1.update_match_score()

# x=readFile("../resources/matches/35612.json")
# print(x[0])
