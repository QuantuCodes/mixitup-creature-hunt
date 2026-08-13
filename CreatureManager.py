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

        subtitle = ttk.Label(
            main,
            text="Manage Creatures for Stream Redeem"
        )
        subtitle.pack(anchor="w", pady=(0, 20))

        content = ttk.Frame(main)
        content.pack(fill="both", expand=True)

        testMsg = ttk.Label(
            content,
            text="Hello Tkinter World",
            font=("Arial", 20)
        )
        testMsg.pack(expand=True)

    def loadData(self):
        if os.path.exists(CREATURES_JSON):
            with open(CREATURES_JSON, "r", encoding="utf-8") as file:
                self.data = json.load(file)
                print("Data loaded") #for debug
        else:
            self.data = {}
            print("JSON not found.") #for debug purposes

app = CreatureManager()
app.mainloop()

