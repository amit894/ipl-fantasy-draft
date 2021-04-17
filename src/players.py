from os import listdir
from os.path import isfile, join
from teams import Teams
from files import readFile, writeFile, appendFile

class Players(Teams):
    def __init__(self,teams):
        super().__init__(teams)

    def get_stats(self):
        for teams in self.get_teams():
            team=readFile("../resources/teams/"+teams)
            for match in team:
                for innings in team[match]:
                    for player in innings:
                        print(jsonify(innings[player]))
                        print("De Limiter")

teams = [f for f in listdir("../resources/teams") if isfile(join("../resources/teams", f))]
P1=Players(teams)
P1.get_stats()
