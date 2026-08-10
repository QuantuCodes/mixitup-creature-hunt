import json
import random
#import sys potentially

#locate + open JSON data file in read
with open("Creatures.JSON", "r", encoding="utf-8") as file:
    data = json.load(file)

#select random creature from JSON (in O(1); dictionary)
creatureName = random.choice(list(data.keys()))
chosen = data[creatureName]

#output respective message for chosen creature
print(chosen["message"])
