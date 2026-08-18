import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

CREATURES_JSON = "Creatures.JSON"

class CreatureManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Creature Manager")
        self.geometry("1280x720")
        self.minsize(512, 288)
        self.darkMode = False

        self.data = {}

        self.loadData()
        self.buildUI()
        self.applyTheme()

        if self.loadError:
            self.after(100, self.showLoadError)

        self.protocol("WM_DELETE_WINDOW", self.onCloseApp)

    def buildUI(self):
        main = ttk.Frame(self, padding=16)
        main.pack(fill="both", expand=True)

        topBar = ttk.Frame(main)
        topBar.pack(fill="x", pady=(0, 20))

        titleColumn = ttk.Frame(topBar)
        titleColumn.pack(side="left", anchor="w")

        title = ttk.Label(
            titleColumn,
            text="Creature Manager",
            font=("Arial", 24, "bold")
        )
        title.pack(anchor="w")

        subtitle = ttk.Label(
            titleColumn,
            text="Manage Creatures for Stream Redeem"
        )
        subtitle.pack(anchor="w", pady=(0, 20))

        self.settingsButton = ttk.Button(topBar, text="\u2699", width=3, command=self.openSettingsMenu)
        self.settingsButton.pack(side="right", anchor="ne")

        content = ttk.Frame(main)
        content.pack(fill="both", expand=True)

        #LHS; JSON entry listbox + scrollbar
        self.leftPanel = ttk.Frame(content, width=320, relief="solid", borderwidth=2)
        self.leftPanel.pack(side="left", fill="y")
        self.leftPanel.pack_propagate(False) #i.e. fixed width

        headerRowLeft = ttk.Frame(self.leftPanel)
        headerRowLeft.pack(fill="x")

        listLabel = ttk.Label(headerRowLeft, text="Creatures")
        listLabel.pack(side="left", anchor="w")

        self.addButton = ttk.Button(headerRowLeft, text="+", width=3, command=self.onAddCreature)
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

        headerRowRight = ttk.Frame(self.rightPanel)
        headerRowRight.pack(fill="x", pady=(0,12)) 

        self.nameHeader = ttk.Label(headerRowRight, text="Select a creature",  font=("Arial", 16, "bold"))
        self.nameHeader.pack(anchor="w", pady=(0, 12))

        self.renameButton = ttk.Button(headerRowRight, text="Rename", command=self.onRenameCreature)
        self.renameButton.pack(side="right")

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

        self.deleteButton = tk.Button(
            self.rightPanel,
            text="Delete Creature",
            bg="#c93631",
            fg="white",
            command=self.onDeleteCreature
        )
        self.deleteButton.pack(side="bottom", anchor="w", pady=(12,0))

    def loadData(self):
        self.loadError = None   #store potential error so GUI can be built first; bug prevention

        if not os.path.exists(CREATURES_JSON):
            self.data={}
            return
        try:
            with open(CREATURES_JSON, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        except (json.JSONDecodeError, OSError) as exception:
            self.loadError = str(exception)
            self.data = {}

    def showLoadError(self):
        messagebox.showerror(
            "Failed to load Creatures.JSON",
            f"The file could not be read:\n{self.loadError}\n\nStarting with an empty creature list."
        )
        #safety net
        self.focus_force()

    #iffy name - may change later on icl...
    #pass None as a param to clear right hand side
    def loadCreatureIntoUI(self, name):
        entry = self.data.get(name, {}) if name is not None else {}

        self.selectedName = name
        self.nameHeader.config(text=name) if name is not None else self.nameHeader.config(text="Select a creature")

        self.messageText.delete("1.0", tk.END)
        self.messageText.insert("1.0", entry.get("message", ""))

        self.shinyText.delete("1.0", tk.END)
        self.shinyText.insert("1.0", entry.get("shinyMessage", ""))

        self.markSaved(entry.get("message", ""), entry.get("shinyMessage",""))

    def onSelect(self, event=None):
        selection = self.creatureListbox.curselection()
        if not selection:
            return

        newName = self.creatureListbox.get(selection[0])

        if (self.selectedName is not None) and self.hasUnsavedChanges():
            if newName != self.selectedName:
                self.openDiscardConfirmation(newName)
            return

        self.loadCreatureIntoUI(newName)

    def openDiscardConfirmation(self, newName):
        oldName = self.selectedName

        confirmWindow, _, buttonRow = self.buildConfirmWindow(
            "Unsaved Changes",
            f"You have unsaved changes to '{oldName}'.\nDiscard them anyways?"
        )

        discardButton = ttk.Button(
            buttonRow, text="Discard Changes",
            command=lambda: self.discardChangesSwitch(newName, confirmWindow)
        )
        discardButton.pack(side="left", padx=8)

        cancelButton = ttk.Button(
            buttonRow, text="Cancel",
            command=lambda: self.cancelSwitch(oldName, confirmWindow)
        )
        cancelButton.pack(side="left", padx=8)

    def discardChangesSwitch(self, newName, window):
        window.destroy()
        self.loadCreatureIntoUI(newName)

    def cancelSwitch(self, oldName, window):
        window.destroy()

        self.selectInListbox(oldName)


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

        self.writeToJson()

        #update such that save button disappears post-save
        self.markSaved(currentMessage, currentShinyMessage)

    def onAddCreature(self):
        defaultName = "new_creature"
        name = defaultName

        i = 1
        while name in self.data:
            name = f"{defaultName}{i}"
            i += 1

        #write entry data
        self.data[name] = {}
        self.writeToJson()

        #refresh listbox; sort entries on LHS
        self.refreshListbox()

        #autoselect newly added entry (for convinience)
        self.selectInListbox(name)
        self.onSelect() #data to RHS

    def onDeleteCreature(self):
        if self.selectedName is None:
            return
        self.openDeleteConfirmation(self.selectedName)

    def openDeleteConfirmation(self, name):
        confirmWindow, messageLabel, buttonRow = self.buildConfirmWindow(
            "Confirm Delete",
            f"Are you sure you want to delete {name}?"
        )

        yesButton = ttk.Button(
            buttonRow, text="Yes",
            command=lambda: self.confirmDelete(name, confirmWindow, messageLabel, buttonRow)
        )
        yesButton.pack(side="left", padx=8)

        noButton = ttk.Button(buttonRow, text="No", command=confirmWindow.destroy)
        noButton.pack(side="left", padx=8)

    def confirmDelete(self, name, window, messageLabel, buttonRow):
        if name in self.data:
            del self.data[name]

        self.writeToJson()

        #refresh listbox as entry deleted
        self.refreshListbox()

        #clear RHS; selected creature no longer exists
        self.loadCreatureIntoUI(None)

        #remove Y/N buttons + countdown to confirmation window closing
        buttonRow.destroy()
        messageLabel.config(text=f"{name} has been deleted")

        countdownLabel = ttk.Label(window, text="")
        countdownLabel.pack(pady=(0,10))

        self.runDeletionCountdown(window, countdownLabel, 5)

    def runDeletionCountdown(self, window, label, secondsLeft):
        if not window.winfo_exists():
            return

        if secondsLeft <= 0:
            window.destroy()
            return

        label.config(text=f"Window will close in {secondsLeft} seconds")
        window.after(1000, lambda: self.runDeletionCountdown(window, label, secondsLeft-1))

    def onRenameCreature(self):
        if self.selectedName is None:
            return
        self.openRenameWindow(self.selectedName)

    def openRenameWindow(self, oldName):
        renameWindow = tk.Toplevel(self)
        renameWindow.title("Rename Creature")
        renameWindow.geometry("320x160")
        renameWindow.resizable(False, False)
        renameWindow.grab_set()

        renameWindow.configure(background=self.currentBg)

        ttk.Label(renameWindow, text=f"Rename '{oldName}' to:").pack(pady=(20,6))

        nameVar = tk.StringVar(value=oldName)
        nameEntry = ttk.Entry(renameWindow, textvariable=nameVar)
        nameEntry.pack(pady=(0,6))
        nameEntry.select_range(0, tk.END)
        nameEntry.focus_set()

        errorLabel = ttk.Label(renameWindow, text="", foreground="red")
        errorLabel.pack()

        buttonRow = ttk.Frame(renameWindow)
        buttonRow.pack(pady=(10,0))

        confirmButton=ttk.Button(
            buttonRow, text="Rename",
            command=lambda: self.renameCreature(oldName, nameVar.get(), errorLabel, renameWindow)
        )
        confirmButton.pack(side="left", padx=8)

        cancelButton = ttk.Button(buttonRow, text="Cancel", command=renameWindow.destroy)
        cancelButton.pack(side="left", padx=8)

    def renameCreature(self, oldName, newName, errorLabel, window):
        newName = newName.strip()

        #validation; guard cases
        if newName == "":
            errorLabel.config(text="Name cannot be empty")
            return

        if not re.match(r"^[A-Za-z0-9_-]+$", newName):
            errorLabel.config(text="Only letters, numbers, _, and - are allowed")
            return

        if newName != oldName and newName in self.data:
            errorLabel.config(text=f"'{newName}' already exists")
            return

        if newName == oldName:
            window.destroy() #no change...so just...close it.
            return

        #rename procedure
        self.data[newName] = self.data.pop(oldName) #isolate content from key

        self.writeToJson()

        #listbox refresh + reselect creature, note under new name
        self.refreshListbox()
        self.selectInListbox(newName)
        
        self.selectedName = newName
        self.onSelect()

        window.destroy()

    def hasUnsavedChanges(self):
        if self.selectedName is None:
            return False

        currentMessage = self.messageText.get("1.0", "end-1c")
        currentShinyMessage = self.shinyText.get("1.0", "end-1c")

        return (currentMessage != self.originalMessage) or (currentShinyMessage != self.originalShinyMessage)

    def onCloseApp(self):
        if (self.selectedName is not None) and self.hasUnsavedChanges():
            self.openQuitConfirmation()
            return

        self.destroy()

    def openQuitConfirmation(self):
        confirmWindow, _, buttonRow = self.buildConfirmWindow(
            "Unsaved Changes",
            f"You have unsaved changes to '{self.selectedName}'.\nQuit anyways?"
        )

        quitButton = ttk.Button(
            buttonRow, text="Quit",
            command=self.confirmQuit
        )
        quitButton.pack(side="left", padx=8)

        cancelButton=ttk.Button(buttonRow, text="Cancel", command=confirmWindow.destroy)
        cancelButton.pack(side="left", padx=8)

    def confirmQuit(self):
        self.destroy()

    def writeToJson(self):
        with open(CREATURES_JSON, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def refreshListbox(self):
        self.creatureListbox.delete(0, tk.END)
        for creatureName in sorted(self.data.keys()):
            self.creatureListbox.insert(tk.END, creatureName)

    def selectInListbox(self, name):
        sortedNames = sorted(self.data.keys())
        index = sortedNames.index(name)
        self.creatureListbox.selection_clear(0, tk.END)
        self.creatureListbox.selection_set(index)
        self.creatureListbox.see(index)

    def buildConfirmWindow(self, title, message, geometry="340x150"):
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry(geometry)
        window.resizable(False, False)
        window.grab_set()

        window.configure(background=self.currentBg)

        messageLabel = ttk.Label(window, text=message, wraplength=300, justify="center")
        messageLabel.pack(pady=(20,10))

        buttonRow = ttk.Frame(window)
        buttonRow.pack()

        return window, messageLabel, buttonRow

    def markSaved(self, message, shiny):
        self.originalMessage = message
        self.originalShinyMessage = shiny
        self.saveButton.pack_forget()

    def openSettingsMenu(self):
        menu = tk.Menu(self, tearoff=0)

        darkModeLabel = "Enable Light Mode" if self.darkMode else "Enable Dark Mode"
        menu.add_command(label=darkModeLabel, command=self.toggleDarkMode)
        menu.add_separator()
        menu.add_command(label="Reload data from JSON", command=self.onReloadJSON)

        x = self.settingsButton.winfo_rootx()
        y = self.settingsButton.winfo_rooty() + self.settingsButton.winfo_height()
        menu.tk_popup(x,y)

    def toggleDarkMode(self):
        self.darkMode = not self.darkMode
        self.applyTheme()

    def applyTheme(self):
        if self.darkMode:
            bg, fg, fieldBg = "#252525", "#f0f0f0", "#383b3d"
        else:
            bg, fg, fieldBg = "#f0f0f0", "#000000", "#ffffff"

        self.currentBg = bg #use for popup windows

        style = ttk.Style(self)
        try:
            #so, since Tk's default theme can ignore bg color on certain platforms, use clam cos it sees bg. pls change this comment later.
            style.theme_use("clam")
        except tk.TCLEror:
            pass

        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("TButton", background=fieldBg, foreground=fg)
        style.configure("TEntry", fieldbackground=fieldBg, foreground=fg)

        self.configure(background=bg)

        self.messageText.configure(background=fieldBg, foreground=fg, insertbackground=fg)
        self.shinyText.configure(background=fieldBg, foreground=fg, insertbackground=fg)
        self.creatureListbox.configure(background=fieldBg, foreground=fg)

    def onReloadJSON(self):
        pass

app = CreatureManager()
app.mainloop()

