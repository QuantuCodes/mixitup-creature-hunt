import json
import random
#import sys potentially

#locate + open JSON data file in read
with open("Creatures.JSON", "r", encoding="utf-8") as file:
    data = json.load(file)

#select random creature from JSON (in O(1); dictionary)
creatureName = random.choice(list(data.keys()))
chosen = data[creatureName]

#Special "shiny message" based on conditional probability
isShiny = random.random() < (1/4096)

#output respective message for chosen creature
if isShiny and ("shinyMessage" in chosen):
    print(chosen["shinyMessage"])
elif "message" in chosen:
    print(chosen["message"])
else:
    print("You have caught", creatureName)
