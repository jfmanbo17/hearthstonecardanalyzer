# hearthstonecardanalyzer 
Utility to track card "win percentages" defined by percentage win when played in a game in combination with track-o-bot

Usage:python cardanalyzer.py numberofdaysbacktoanalyze trackobot_username trackobot_apikey (hero)

NOTE: WRITTEN IN PYTHON 3

numberofdaystoanalyze determines how far back in your history the program should look. Must be positive integer.

trackobot_username and trackobot_apikey should be copy-pasted from https://trackobot.com/profile/settings/api

hero is an optional argument if you want to restrict the program to look only at games played with a certain class. Note this is case sensitive, i.e. Mage is valid but mage is not. 

The program will print the number of games played within the constraints, and cards along with their "win percentages"

This program is still in development -- more features may be added at a later date, and it is still very possible that you will see python errors if you feed in garbage input.