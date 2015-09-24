import sys
import json
import requests
import time
import datetime

def winfunc(outcome):
	if outcome == "loss":
		return 0
	else:
		return 1

def addcards(dictionary,game):
	cards_played={}
	for turn in game["card_history"]:
		if turn["player"] == "me":
			cards_played[turn["card"]["name"]]=1
	for item in cards_played:
		if item in dictionary:
			dictionary[item] += 1
		else:
			dictionary[item] = 1

def doapage(gamesplayed,historylist,today,dayincrement,dontcheckclass,hero):
	result=1
	for game in historylist:
		gametime = datetime.datetime.strptime(game["added"],"%Y-%m-%dT%H:%M:%S.%fz")
		if (gametime > (today - dayincrement)):
			if (dontcheckclass | (hero == game["hero"])):
				gamesplayed += 1
				if winfunc(game["result"]):
					addcards(windict,game)
				else:
					addcards(lossdict,game)
		else: 
			result=0
	return (result, gamesplayed)

windict={}		
lossdict={}
gamesplayed=0
today = datetime.datetime.now()
numdays = int(sys.argv[1])
username = sys.argv[2]
key = sys.argv[3]
if len(sys.argv)>4:
	hero = sys.argv[4]
	dontcheckclass=0
else:
	hero = ""
	dontcheckclass=1
dayincrement = datetime.timedelta(days=numdays)
page=1
print("page", page)
rawinput=requests.get("https://trackobot.com/profile/history.json?username=" + username + "&token=" + key).text
numpages=json.loads(rawinput)["meta"]["total_pages"]
historylist=json.loads(rawinput)["history"]
(datecheck,gamesplayed)=doapage(gamesplayed,historylist,today,dayincrement,dontcheckclass,hero)

while (page < numpages) & datecheck:
	page += 1
	print("page", page)
	trackourl="https://trackobot.com/profile.json?page=" + str(page) + "&username=" + username + "&token=" + key
	rawinput=requests.get(trackourl).text
	historylist=json.loads(rawinput)["history"]
	(datecheck,gamesplayed)=doapage(gamesplayed,historylist,today,dayincrement,dontcheckclass,hero)

for card in windict:
	if card not in lossdict:
		lossdict[card]=0

for card in lossdict:
	if card not in windict:
		windict[card]=0

print("games played:", gamesplayed)
for card in windict:
	print(card, float(windict[card])/(float(windict[card]+lossdict[card])))


		
		