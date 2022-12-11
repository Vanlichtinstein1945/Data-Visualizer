import tkinter as tk
from tkinter import ttk
from os import path
from src.Utils.DataFrame_Windowed import DataFrame_Windowed
from src.Utils.Constants import SUMMARYFILENAME, SUMMARY_COLUMNS

class TableFrame(tk.Frame):
    """Frame responsible for displaying aggregted data in tabular format"""
    def __init__(self, root, pathToFiles:str, chosenCols=SUMMARY_COLUMNS, patientID=None):
        """Create a new aggregation table frame to display. Can use an existing data frame or create new one to aggregate."""
        self.summaryCsvPath = path.join(pathToFiles, SUMMARYFILENAME)
        self.chosenCols = chosenCols
        self.patientId = patientID

        super().__init__(root, highlightbackground='blue', highlightthickness=2)
        self.label = tk.Label(self, text='Summary Stats for Patient ID: ' + patientID)
        self.label.pack()
        self.root = root
        self.tree = self.createTable()
        self.patientId = patientID


    def createTable(self):
        """Helper for creating the table with aggregated data"""
        df_windowed = DataFrame_Windowed(self.summaryCsvPath, colsToKeep=self.chosenCols)

        #Aggregate data, round to 2 decimal places
        summaryStats = df_windowed.Aggregate().round(2)

        #Store column in list to loop over later
        dfCols = summaryStats.columns

        #insert empty space so top left corner is empty, convert column index to list
        dfCols = list(dfCols.insert(0,''))

        #Convert to appropriate format - add column for the count type names in the 0th column
        rowHeaders = ['Count','Mean','STD','Min','25%','50%','75%','Max']
        summaryStats.insert(loc=0, column='type', value=rowHeaders)

        #Convert data to list - easier to import into Tkinter frame
        summaryStats = summaryStats.values.tolist()

        #create tree
        tree = ttk.Treeview(self, columns=dfCols, show='headings')

        #Title for tree

        #create headers, set column width
        for colHead in dfCols:
            tree.heading(colHead, text=colHead)
            tree.column(column=colHead, width=120)

        #add data
        for obs in summaryStats:
            tree.insert('', tk.END, values=obs)

        #create tree grid, place on root window
        tree.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        return tree
