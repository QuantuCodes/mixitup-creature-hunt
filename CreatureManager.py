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

        self.leftPanel = ttk.Frame(content, width=320, relief="solid", borderwidth=2)
        self.leftPanel.pack(side="left", fill="y")
        self.leftPanel.pack_propagate(False) #i.e. fixed width

        listLabel = ttk.Label(self.leftPanel, text="Creatures")
        listLabel.pack(anchor="w")

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

        self.rightPanel = ttk.Frame(content, padding=(20, 0, 0, 0), relief="solid", borderwidth=2)
        self.rightPanel.pack(side="left", fill="both", expand=True)

    def loadData(self):
        if os.path.exists(CREATURES_JSON):
            with open(CREATURES_JSON, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        else:
            self.data = {}

    def onSelect(self, event=None):
        pass

app = CreatureManager()
app.mainloop()

