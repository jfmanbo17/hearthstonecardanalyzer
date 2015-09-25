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

def doapage(gamesplayed,historylist,today,dayincrement,dontcheckclass,hero,win_total,loss_total):
	result=1
	for game in historylist:
		gametime = datetime.datetime.strptime(game["added"],"%Y-%m-%dT%H:%M:%S.%fz")
		if (gametime > (today - dayincrement)):
			if (dontcheckclass | (hero == game["hero"])):
				gamesplayed += 1
				if winfunc(game["result"]):
					win_total += 1
					addcards(windict,game)
				else:
					loss_total += 1
					addcards(lossdict,game)
		else: 
			result=0
	return (result, gamesplayed, win_total, loss_total)

win_total=0
loss_total=0
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
print("Loading Page", page)
rawinput=requests.get("https://trackobot.com/profile/history.json?username=" + username + "&token=" + key).text
numpages=json.loads(rawinput)["meta"]["total_pages"]
historylist=json.loads(rawinput)["history"]
(datecheck,gamesplayed,win_total,loss_total)=doapage(gamesplayed,historylist,today,dayincrement,dontcheckclass,hero,win_total,loss_total)

while (page < numpages) & datecheck:
	page += 1
	print("Loading Page", page)
	trackourl="https://trackobot.com/profile.json?page=" + str(page) + "&username=" + username + "&token=" + key
	rawinput=requests.get(trackourl).text
	historylist=json.loads(rawinput)["history"]
	(datecheck,gamesplayed)=doapage(gamesplayed,historylist,today,dayincrement,dontcheckclass,hero,win_total,loss_total)

for card in windict:
	if card not in lossdict:
		lossdict[card]=0

for card in lossdict:
	if card not in windict:
		windict[card]=0

def percentValue(card):
	return float(windict[card])/(float(windict[card]+lossdict[card]))

def percentNiceFormat(number):
	return "%6.2f%%" % (100 * number)

max_width_card = max([len(card) for card in windict])
if (max_width_card < 4):
	max_width_card = 4
	
max_width_number = max([len(str(windict[card]+lossdict[card])) for card in windict])

if (max_width_number < 4):
	max_width_number = 4

print("Games played:", gamesplayed)
print("Overall Winrate:", percentNiceFormat(float(win_total) / float(win_total + loss_total)))

print ("/", ("-" * (max_width_card + 6 + max_width_number + 7)), "\\")
print ("| {0:<{col1}} | {1:<{col2}} ({2:>{col3}}) |".format("Card", "Winrate", "Seen", col1=max_width_card, col2=6, col3=max_width_number))
print ("|","=" * (max_width_card + 6 + max_width_number + 7) ,"|")

divider = 0

for card in sorted(windict, key=percentValue, reverse = True):
	if (not divider and percentValue(card) < float(win_total) / float(win_total + loss_total)):
		print("|","-" * (max_width_card + 6 + max_width_number + 7),"|")
		divider = 1
	print("| {0:<{col1}} | {1:<{col2}} ({2:>{col3}}) |".format(card, percentNiceFormat(percentValue(card)), windict[card]+lossdict[card], col1 = max_width_card, col2 = 6, col3 = max_width_number))

print ("\\", ("-" * (max_width_card + 6 + max_width_number + 7)), "/")
