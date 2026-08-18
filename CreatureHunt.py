import json
import random
import sys


FLEE_CHANCE = 20/100
#chance creature flees
hasFled = random.random() < (FLEE_CHANCE)
if hasFled:
    print("Oh. It fled. Sorry.")
    sys.exit()

#locate + open JSON data file in read
with open("Creatures.JSON", "r", encoding="utf-8") as file:
    data = json.load(file)

#select random creature from JSON (in O(1); dictionary)
creatureName = random.choice(list(data.keys()))
chosen = data[creatureName]

#Special "shiny message" based on conditional probability
isShiny = random.random() < ((1 - FLEE_CHANCE) * 1/4096)

#output respective message for chosen creature
if isShiny and ("shinyMessage" in chosen):
    print(chosen["shinyMessage"])
elif "message" in chosen:
    print(chosen["message"])
else:
    print("You have caught", creatureName)