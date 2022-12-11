import tkinter as tk
from tkinter.ttk import Notebook
from src.Frame.DataBuilderFrame import DataBuilderFrame

class Window(tk.Tk):
    def __init__(self, apptitle, pathToDatasets):
        """Creates a top-level window for the application responsible for the notebook and window geometry."""
        super().__init__()
        self.title(apptitle)
        self.geometry('1200x900')

        self.notebook = Notebook(self)

        data_builder_tab = DataBuilderFrame(self.notebook, pathToDatasets)
        self.notebook.add(data_builder_tab, text='Data Builder')
        self.notebook.pack(fill=tk.BOTH, expand=True)
