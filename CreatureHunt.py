import json
import random
#import sys potentially

with open("Creatures.JSON", "r", encoding="utf-8") as file:
    data = json.load(file)

print(data)
