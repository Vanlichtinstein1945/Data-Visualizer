import tkinter as tk
from tkinter import messagebox
from src.Frame.SelectUserAndDateFrame import SelectUserAndDateFrame
from src.Frame.ColumnSelectorFrame import ColumnSelectorFrame
from src.Frame.VisualizerFrame import VisualizerFrame
from src.Frame.TableFrame import TableFrame

DISPLAYTIMEOPTIONS=('Datetime (UTC)', 'Datetime (Local)')

class DataBuilderFrame(tk.Frame):
    """ User interface for configuring dataset and options to load in"""
    def __init__(self, notebook, pathToDatasets):
        """Creates a frame responsible for handling user input and selection for loading datasets"""
        super().__init__(notebook, highlightbackground="black", highlightthickness=1)
        self.notebook = notebook

        self.fileSelectorFrame = SelectUserAndDateFrame(self, pathToDatasets)
        self.fileSelectorFrame.pack(side=tk.LEFT, anchor=tk.NW, expand=False, padx=5, pady=5)

        self.columnSelectorFrame = ColumnSelectorFrame(self)
        self.columnSelectorFrame.pack(side=tk.LEFT, anchor=tk.N, padx=165, pady=5)

        self.createVisualButton = tk.Button(self, text="Create Visual", command=self.CreateVisual)
        self.createVisualButton.pack(side=tk.TOP, anchor=tk.E, pady=5)

        self.createTableButton = tk.Button(self, text="Create Summary", command=self.CreateSummary)
        self.createTableButton.pack(anchor=tk.E, pady=5)

        self.displayTimeSetIndex = 0
        self.displayTimeButtonStringVar = tk.StringVar()
        self.displayTimeButtonStringVar.set(DISPLAYTIMEOPTIONS[0])
        self.setDisplayTimeButton = tk.Button(self, textvariable=self.displayTimeButtonStringVar, command=self.SwitchTime)
        self.setDisplayTimeButton.pack(anchor=tk.E, pady=5)

        self.numberOfVisuals = 0
        self.numberOfTables = 0


    def SwitchTime(self):
        """Callback for Toggling Type of Time to Display"""
        # toggling here
        self.displayTimeSetIndex ^= 1
        self.displayTimeButtonStringVar.set(DISPLAYTIMEOPTIONS[self.displayTimeSetIndex])


    def CreateSummary(self):
        """Button Command Callback To Generate a New Visual Based on User Config"""
        pathToFiles = self.fileSelectorFrame.GetPathToFiles()
        chosenCols = self.columnSelectorFrame.GetChosenColumns()
        patientId = self.fileSelectorFrame.GetPatientId()

        if not pathToFiles:
            messagebox.showwarning('Data Build Failure', 'Must select a patient date and id (both should highlight blue).')
            return

        if len(chosenCols) == 0:
            messagebox.showwarning('Data Summary Failure', 'Please add one or more time series columns to import for summary.')
            return

        table_frame = TableFrame(self.notebook, pathToFiles, chosenCols, patientID=patientId)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.numberOfTables += 1
        self.notebook.add(table_frame, text=f'Table {self.numberOfTables}')


    def CreateVisual(self):
        """Button Command Callback To Generate a New Visual Based on User Config"""
        pathToFiles = self.fileSelectorFrame.GetPathToFiles()
        chosenCols = self.columnSelectorFrame.GetChosenColumns()
        timeColumn = DISPLAYTIMEOPTIONS[self.displayTimeSetIndex]
        patientId = self.fileSelectorFrame.GetPatientId()

        if not pathToFiles:
            messagebox.showwarning('Data Build Failure', 'Must select a patient date and id (both should highlight blue).')
            return

        if len(chosenCols) == 0:
            messagebox.showwarning('Visualization Build Failure', 'Please add one or more time series columns to import for visualization.')
            return

        # Create Visual Frame
        # Add To Notebook, Maybe Set That Tab as active
        visual_frame = VisualizerFrame(self.notebook, pathToFiles, chosenCols, timeColumn, patientId)
        visual_frame.pack(fill=tk.BOTH, expand=True)

        self.numberOfVisuals += 1
        self.notebook.add(visual_frame, text=f'Visual {self.numberOfVisuals}')
        
