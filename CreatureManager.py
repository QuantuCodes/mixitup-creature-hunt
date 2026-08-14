import tkinter as tk
from tkinter import ttk
import json
import os

CREATURES_JSON = "Creatures.JSON"

class CreatureManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Creature Manager")
        self.geometry("1280x720")
        self.minsize(512, 288)

        self.data = {}

        self.loadData()
        self.buildUI()

    def buildUI(self):
        main = ttk.Frame(self, padding=16)
        main.pack(fill="both", expand=True)

        title = ttk.Label(
            main,
            text="Creature Manager",
            font=("Arial", 24, "bold")
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            main,
            text="Manage Creatures for Stream Redeem"
        )
        subtitle.pack(anchor="w", pady=(0, 20))

        content = ttk.Frame(main)
        content.pack(fill="both", expand=True)

        #LHS; JSON entry listbox + scrollbar
        self.leftPanel = ttk.Frame(content, width=320, relief="solid", borderwidth=2)
        self.leftPanel.pack(side="left", fill="y")
        self.leftPanel.pack_propagate(False) #i.e. fixed width

        headerRow = ttk.Frame(self.leftPanel)
        headerRow.pack(fill="x")

        listLabel = ttk.Label(headerRow, text="Creatures")
        listLabel.pack(side="left", anchor="w")

        self.addButton = ttk.Button(headerRow, text="+", width=3, command=self.onAddCreature)
        self.addButton.pack(side="right")

        listFrame = ttk.Frame(self.leftPanel)
        listFrame.pack(fill="both", expand=True)

        self.creatureListbox = tk.Listbox(listFrame, exportselection=False)
        self.creatureListbox.pack(side="left", fill="both", expand=True)
        self.creatureListbox.bind("<<ListboxSelect>>", self.onSelect)

        scrollbar = ttk.Scrollbar(listFrame, orient="vertical", command=self.creatureListbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.creatureListbox.config(yscrollcommand=scrollbar.set)

        for name in sorted(self.data.keys()):
            self.creatureListbox.insert(tk.END, name)

        #RHS; JSON entry editor
        self.rightPanel = ttk.Frame(content, padding=(20, 0, 0, 0), relief="solid", borderwidth=2)
        self.rightPanel.pack(side="left", fill="both", expand=True)

        self.nameHeader = ttk.Label(self.rightPanel, text="Select a creature",  font=("Arial", 16, "bold"))
        self.nameHeader.pack(anchor="w", pady=(0, 12))

        ttk.Label(self.rightPanel, text="Message:").pack(anchor="w")
        self.messageText = tk.Text(self.rightPanel, height=4, wrap="word")
        self.messageText.pack(fill="x", pady=(0, 12))
        self.messageText.bind("<KeyRelease>", self.checkForChanges)

        ttk.Label(self.rightPanel, text="ShinyMessage:").pack(anchor="w")
        self.shinyText = tk.Text(self.rightPanel, height=4, wrap="word")
        self.shinyText.pack(fill="x", pady=(0, 12))
        self.shinyText.bind("<KeyRelease>", self.checkForChanges)

        self.selectedName = None

        self.saveButton = ttk.Button(self.rightPanel, text="Save Changes", command=self.saveChanges)

    def loadData(self):
        if os.path.exists(CREATURES_JSON):
            with open(CREATURES_JSON, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        else:
            self.data = {}

    def onSelect(self, event=None):
        selection = self.creatureListbox.curselection()
        if not selection:
            return

        name = self.creatureListbox.get(selection[0])
        entry = self.data.get(name, {})

        self.selectedName = name
        self.nameHeader.config(text=name)

        self.messageText.delete("1.0", tk.END)
        self.messageText.insert("1.0", entry.get("message", ""))

        self.shinyText.delete("1.0", tk.END)
        self.shinyText.insert("1.0", entry.get("shinyMessage", ""))

        #store original entries for change detection/s
        self.originalMessage = entry.get("message","")
        self.originalShinyMessage = entry.get("shinyMessage", "")

    def checkForChanges(self, event=None):
        if self.selectedName is None:
            return

        currentMessage = self.messageText.get("1.0", "end-1c")
        currentShinyMessage = self.shinyText.get("1.0", "end-1c")

        changed = (currentMessage != self.originalMessage) or (currentShinyMessage != self.originalShinyMessage)
        if changed:
            self.saveButton.pack(anchor="e", pady=(6, 0))
        else:
            self.saveButton.pack_forget()

    def saveChanges(self):
        if self.selectedName is None:
            return

        currentMessage = self.messageText.get("1.0", "end-1c")
        currentShinyMessage = self.shinyText.get("1.0", "end-1c")

        entry = {}
        if currentMessage:
            entry["message"] = currentMessage
        if currentShinyMessage:
            entry["shinyMessage"] = currentShinyMessage
        self.data[self.selectedName] = entry

        with open(CREATURES_JSON, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

        #update such that save button disappears post-save
        self.originalMessage = currentMessage
        self.originalShinyMessage = currentShinyMessage
        self.saveButton.pack_forget()

    def onAddCreature(self):
        defaultName = "new_creature"
        name = defaultName

        i = 1
        while name in self.data:
            name = f"{defaultName}{i}"
            i += 1

        #write entry data
        self.data[name] = {}
        with open(CREATURES_JSON, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

        #refresh listbox; sort entries on LHS
        self.creatureListbox.delete(0, tk.END)
        for creatureName in sorted(self.data.keys()):
            self.creatureListbox.insert(tk.END, creatureName)

        #autoselect newly added entry (for convinience)
        sortedNames = sorted(self.data.keys())
        newIndex = sortedNames.index(name)
        self.creatureListbox.selection_clear(0, tk.END)
        self.creatureListbox.selection_set(newIndex)
        self.creatureListbox.see(newIndex) #may be off screen, so scroll to
        self.onSelect() #data to RHS


app = CreatureManager()
app.mainloop()

