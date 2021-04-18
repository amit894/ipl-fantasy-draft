import requests
import flask
import json
import flask
import re
from bs4 import BeautifulSoup
import json
from pprint import pprint
from collections import Counter
from files import readFile, writeFile

def get_match(url,teams):

  innings=[]
  result={}
  Scorecard = requests.get(url).text
  Soup = BeautifulSoup(Scorecard,"html.parser")
  for i in range(2):
      current_innings=[]
      batting=[]
      bowling=[]
      fielding=[]
      current_innings=get_innings(Soup, "innings_"+str(i+1))
      innings.append(current_innings)
      batting.append(get_batting(innings[i][0]))
      bowling.append(get_bowling(innings[i][1]))
      fielding.append(get_fielding(batting))
      result[teams[i]+"_innings_"+str(i+1)+"_batting"]=batting
      result[teams[1-i]+"_innings_"+str(i+1)+"_bowling"]=bowling
      result[teams[1-i]+"_innings_"+str(i+1)+"_fielding"]=fielding
  return result


def get_innings(Soup,Innings):
    Inning_info=[]
    Inning = Soup.find_all('div',id=Innings)[0]
    Inning_batting = Inning.find_all('div',class_="cb-col cb-col-100 cb-ltst-wgt-hdr")[0]
    Inning_bowling = Inning.find_all('div',class_="cb-col cb-col-100 cb-ltst-wgt-hdr")[1]
    Inning_batting = Inning_batting.find_all('div',class_="cb-col cb-col-100 cb-scrd-itms")
    Inning_bowling = Inning_bowling.find_all('div',class_="cb-col cb-col-100 cb-scrd-itms")
    Inning_info.append(Inning_batting)
    Inning_info.append(Inning_bowling)
    return Inning_info

def get_batting(Inning_batting):
    batting_info=[]
    for b in Inning_batting:
        batsman = {}
        name = b.find('a',class_="cb-text-link")
        if name:
            pid = name['href'][10:]
            batsman['pid'] = str(pid[:pid.find('/')])
            batsman['name'] = str(name.get_text()).strip()
        if 'name' in batsman:
            if '(' in batsman['name']:
                batsman['name'] = batsman['name'][:batsman['name'].find('(')].strip()
            out_by = b.find('span',class_="text-gray")
            if out_by:
                batsman['out_by'] = str(out_by.get_text()).strip()
                runs = b.find('div',class_="cb-col cb-col-8 text-right text-bold")
            if runs:
                 batsman['runs'] = str(runs.get_text()).strip()
                 all_others = b.find_all('div',class_="cb-col cb-col-8 text-right")
            if len(all_others)>0:
                batsman['balls'] = str(all_others[0].get_text()).strip()
                batsman['fours'] = str(all_others[1].get_text()).strip()
                batsman['sixes'] = str(all_others[2].get_text()).strip()
                batsman['sr'] = str(all_others[3].get_text()).strip()

            if len(batsman) > 0:
                batting_info.append(batsman)
    return batting_info

def get_bowling(Inning_bowling):
    bowling_info=[]
    for b in Inning_bowling:
        bowler = {}
        name = b.find('a',class_="cb-text-link")
        if name:
            pid = name['href'][10:]
            bowler['pid'] = str(pid[:pid.find('/')])
            bowler['name'] = str(name.get_text()).strip()
        if 'name' in bowler:
            if '(' in bowler['name']:
                bowler['name'] = bowler['name'][:bowler['name'].find('(')].strip()
            wickets = b.find('div',class_="cb-col cb-col-8 text-right text-bold")
            if wickets:
                bowler['wickets'] = str(wickets.get_text()).strip()
                runs_given = b.find_all('div',class_="cb-col cb-col-10 text-right")
            if runs_given:
                bowler['runs_given'] = str(runs_given[0].get_text()).strip()
                bowler['ec'] = str(runs_given[1].get_text()).strip()
                all_others = b.find_all('div',class_="cb-col cb-col-8 text-right")
            if len(all_others)>0:
                bowler['overs'] = str(all_others[0].get_text()).strip()
                bowler['maiden'] = str(all_others[1].get_text()).strip()
                bowler['no_balls'] = str(all_others[2].get_text()).strip()
                # bowler['wides'] = str(all_others[3].get_text()).strip()


            if len(bowler) > 0:
                bowling_info.append(bowler)
    return bowling_info

def get_fielding(Inning_batting):
    fielding_info={}
    fielders=[]
    for i in range(len(Inning_batting[0])):
        mode=''
        if 'out_by' in Inning_batting[0][i]:
            dismissal=Inning_batting[0][i]['out_by']
        if dismissal.find("c and b") == 0:
            fielders.append(dismissal.split("c and b")[1].strip())
        elif dismissal.find("c") == 0:
            fielders.append(dismissal.split("c ")[1].split("b ")[0].strip())
        if dismissal.find("st") == 0:
            fielders.append(dismissal.split("st ")[1].split("b ")[0].strip())
        if dismissal.find("run out") == 0:
            fielders.extend([x.strip() for x in dismissal.split("run out")[1].replace('(', '').replace(')', '').split("/")])
        if dismissal.find("sub (") != -1:
                del fielders[-1]
    fielding_info=Counter(fielders)
    temp_list=[]
    for keys in fielding_info:
        temp_dict={}
        temp_dict[keys]=fielding_info[keys]
        temp_list.append(temp_dict)
    return(temp_list)

#print(get_match("https://www.cricbuzz.com/live-cricket-scorecard/35632/rr-vs-dc-7th-match-indian-premier-league-2021",["dc","rr"]))
