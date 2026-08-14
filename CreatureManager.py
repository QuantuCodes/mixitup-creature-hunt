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

        #RHS; JSON entry editor
        self.rightPanel = ttk.Frame(content, padding=(20, 0, 0, 0), relief="solid", borderwidth=2)
        self.rightPanel.pack(side="left", fill="both", expand=True)

        self.nameHeader = ttk.Label(self.rightPanel, text="Select a creature",  font=("Arial", 16, "bold"))
        self.nameHeader.pack(anchor="w", pady=(0, 12))

        ttk.Label(self.rightPanel, text="Message:").pack(anchor="w")
        self.messageText = tk.Text(self.rightPanel, height=4, wrap="word")
        self.messageText.pack(fill="x", pady=(0, 12))

        ttk.Label(self.rightPanel, text="ShinyMessage:").pack(anchor="w")
        self.shinyText = tk.Text(self.rightPanel, height=4, wrap="word")
        self.shinyText.pack(fill="x", pady=(0, 12))

        self.selectedName = None

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

app = CreatureManager()
app.mainloop()

