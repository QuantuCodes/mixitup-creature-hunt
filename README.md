# Creature Hunt & Creature Manager
This repository includes a two-part tool for running a "Hunt for Creatures"-style Twitch channel point redeem. Inside are two executable files: CreatureHunt.py, which will be linked to the redeem in MixItUp (further detail provided later), and CreatureManager.py, a friendly GUI to ensure that managing the creature pool is as accessible as possible.

## Files
Provided below is a table which describes each file in this repository, and breadth on how to use it.
| File Name | Intended Purpose |
|-----------|------------------|
| CreatureManager.py | GUI app for adding, editing, renaming, and deleting creatures. Used ideally outside of stream. |
| CreatureHunt.py | The script which MixItUp runs on redeem. Picks a random creature, rolls flee/shiny odds, and outputs the result|
| Creatures.JSON | The data file both scripts read to and/or write from. Created automatically the first time a creature is saved in the manager |

## Requirements
- Python 3.8/newer
- tkinter - included with most python installs by default. If the Manager fails to launch with a `ModuleNotFoudnError: No module named 'tkinter`, then this should be installed separately. Windows/MAC has it bundled with Python, whilst Linux users should `sudo apt install python3-tk`.
- No other 3rd party packages required, as all other libraries are included in Python's standard library. For documentation sake, they are listed as follows: json, random, sys, os, re, (tkinter).

## First-time Setup
1. Put CreatureManager.py and CreatureHunt.py in the same folder.
2. Run CreatureManager.py and add at least one creature before going live (see the "+" on the Left Hand Side).
3. Ensure this creature has been added AND saved, as if the redeem is fired before this entry is made, then a File-not-found error will occur. Adding a creature through the manager creates the file automatically, so ensure that this occurs before a user can redeem the respective redeem. 
4. Confirm the two scripts are pointed at the same Creatures.JSON - both currently expect it in the same folder of which they are ran from.

Note: Step 3 may be looked at soon, to potentially automatically create a creature upon opening CreatureManager if Creatures.JSON is empty/doesnt exist. However, for now, please follow the procedure that has been described above. Thank you :)

## Using Creature Manager
- Adding a creature: click "+" in the top-left. New entries are auto-named "new-creature1", "new-creature2", ..., "new-creature(n)" for n new entries. This is to avoid collisions.
- Editing a creature: click on the creature's name in the given list (see the left of the screen), and you will be shown the current contents of this creature entry on the right of the screen. You can edit not only the Message and ShinyMessage boxes, but also the creature's name itself.
- Message vs ShinyMessage: Message will be outputted upon a normal result from CreatureHunt.py. ShinyMessage will be outputted for a creature if the shiny check has succeeded in CreatureHunt.py. By default, if no message or shiny message is defined, the default "You have caught _CreatureName_" will be outputted. 
- Renaming: click 'Rename' next to the creature's name. Only letters (both cases), numbers, "_", and "-" are permitted. Duplicate names are also blocked.
- Deleting: the red 'Delete Creature' button asks for delete confirmation, then will show a 5 second countdown before the window closes (upon confirming).
- Switching creatures with unsaved edits: this application will always ask before discarding unsaved changes, whether due to clicking a different creature, closing the application, or reloading the JSON (in case of external editing).
- Settings ('⚙', in the top right):
    - Toggle Dark Mode: visual change only, with no effect on data.
    - Reload from JSON: re-reads Creatures.JSON and refreshes the application. Useful if the file was edited manually outside of the app. Warns first if you have unsaved edits.

## How CreatureHunt.py works
Each time a twitch-user hits the redeem in chat, MixItUp will run CreatureHunt.py, which does the following:
1. Flee Check: currently, the code dictates a 20% chance that the creature will flee, thus returning a message reflecting this. Both FLEE_CHANCE and this message can be altered if it is wished so.
2. Pick a creature: a random creature is chosen from every entry in Creatures.JSON, each equally likely P(chosen)=1/n.
3. Shiny check: completely independent of which creature is chosen, there is a hard-coded 1/4096 chance that the selected creature will in turn be shiny, outputting the shinyMessage instead. If no shiny message exists, then it will simply output the regular message, or default message.
4. Output: A shiny encounter that has a defined shinyMessage with it will output the shinyMessage as stated above. Otherwise, the regular message prints. If neither field is defined, the default "You have caught _name_" is outputted.

## How shiny odds work.
...Will adjust this later.

## ⚠️ MUST DO's before going live
Please confirm that:
1.The creature pool has not been set to zero. This can be viewed in the CreatureManager. At least one entry at a time must be ensured.
2. MixItUp wiring is not YET covered by this readme. Will occur very soon.

## Known limitations
- No confirmation prompt if JSON pool is manually edited (i.e outside the manager). Malformed entries are silently be skipped over by .get() fallbacks rather than causing an error, so a typo'd error will simply raise a visible warning.
- CreatureManager.py and CreatureHunt.py don't coordinate file access. In other words, there is a window where, if editing the creature pool live, the user could redeem against a half-written entry. Concurrent access and Isolation (from ACID) will be implemented later on. Please bare with.

## Extra information - Project origins
A streamer reached out to me regarding their existing twitch redeem, being Mesian Velari's "Shiny Wooper Hunt". The original text file and endless lines of elif selection statements with O(n) access also was asking for a little upgrade, for lack of better phrasing (I'm sort of tired I'd like to sleep - sorry! ill fix this). Thus the O(1) solution was very quickly born. CreatureManager.py only came to exist as I thought I'd save Mesian from having to learn JSON.


