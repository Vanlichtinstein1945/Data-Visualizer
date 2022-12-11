import tkinter as tk
from src.Utils.Constants import TIME_SERIES_COLUMNS

class ColumnSelectorFrame(tk.Frame):
    """Responsible for Creating Two Listboxes and Two Buttons to Select Which Columns to Load For Visualization"""
    def __init__(self, root):
        super().__init__(root, highlightbackground="black", highlightthickness=0.5)
        self.root = root
        self.unchosenCols = [col for col in TIME_SERIES_COLUMNS]
        self.unchosenCols.sort()
        self.chosenCols = []
        self.unchosenColsVar = tk.StringVar(value=self.unchosenCols)
        self.chosenColsVar = tk.StringVar(value=self.chosenCols)

        self.label = tk.Label(self, text='Select Columns To Plot')
        self.label.pack(side=tk.TOP, expand=False, fill=tk.NONE)

        self.unchoseColListbox = tk.Listbox(self, selectmode=tk.SINGLE, listvariable=self.unchosenColsVar)
        self.unchoseColListbox.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)
        self.choseColListbox = tk.Listbox(self, selectmode=tk.SINGLE, listvariable=self.chosenColsVar)
        self.choseColListbox.pack(side=tk.LEFT, expand=False, fill=tk.BOTH)

        self.addColButton = tk.Button(self, text="Add Column", command=self.AddColumn)
        self.addColButton.pack()
        self.removeColButton = tk.Button(self, text="Remove Column", command=self.RemoveColumn)
        self.removeColButton.pack()


    def AddColumn(self):
        """Button Command For Adding Selected Columns"""
        try:
            selected_index = self.unchoseColListbox.curselection()[0]
        except IndexError:
            return

        col = self.unchoseColListbox.get(selected_index)
        self.chosenCols.append(col)
        self.unchosenCols.remove(col)
        self.UpdateView()


    def RemoveColumn(self):
        """Button Command For Removing Selected Columns"""
        try:
            selected_index = self.choseColListbox.curselection()[0]
        except IndexError:
            return

        col = self.choseColListbox.get(selected_index)
        self.unchosenCols.append(col)
        self.chosenCols.remove(col)
        self.UpdateView()


    def UpdateView(self):
        """Helper Function to Update Listbox Views By Setting Tk String Vars"""
        self.unchosenCols.sort()
        self.chosenCols.sort()
        self.unchosenColsVar.set(self.unchosenCols)
        self.chosenColsVar.set(self.chosenCols)
    

    def GetChosenColumns(self):
        """Returns a copy of the selected columns"""
        if len(self.chosenCols) == 0:
            print('Warning: No columns selected to import. Notifying User...')

        return self.chosenCols[:]