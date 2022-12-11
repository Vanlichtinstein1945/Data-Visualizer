import tkinter as tk
from os import path
import pandas as pd
from src.Utils.DataFrame_Windowed import DataFrame_Windowed
from src.Utils.Constants import SUMMARYFILENAME, METADATAFILENAME
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as dates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import RangeSlider

class GraphManager():
    """Responsible for managing a set of plots"""
    def __init__(self, root, pathToSummaryCsv, chosenCols, timeColumn):
        self.root = root
        self.df_windowed = DataFrame_Windowed(pathToSummaryCsv, chosenCols)
        self.SetupGraphs(timeColumn=timeColumn)


    def SetupGraphs(self, timeColumn='Datetime (UTC)'):
        """Create matplotlib graph, plot points, and display to window"""
        self.df = self.df_windowed.GetDataFrame()
        
        self.numberOfGraphs = len(self.df_windowed.GetSelectedColumns())
        print(f'Number of Graphs Generated: {self.numberOfGraphs}')

        figure, axs = plt.subplots(1, self.numberOfGraphs, sharex=True)

        print("Before: ", self.df['Datetime (UTC)'].iloc[-1])
        self.df['Datetime (UTC)'] = pd.to_datetime(self.df['Datetime (UTC)'], utc=True, format="%H:%M:%S")
        #pd.to_datetime(df['Datetime (UTC)'], utc=True, inplace=True)
        print("After: ", self.df['Datetime (UTC)'].iloc[-1])

        self.df[timeColumn] = pd.to_datetime(self.df[timeColumn], utc=True, format="%H:%M:%S")

        #df['Datetime (UTC)'] = dates.date2num(df['Datetime (UTC)'])
        
        #xlocator = dates.HourLocator(byhour=range(0, 24, 1))

        self.figure = figure
        self.axs = axs

        self.df[timeColumn] = pd.to_datetime(self.df[timeColumn], format="%H:%M:%S")
       
        print("type: ", self.df[timeColumn].dtype)

        self.df.sort_values(timeColumn, inplace=True)
        self.df.reset_index(drop=True, inplace=True)

        #For the slider steps
        self.granularity = 5 # in minutes
        
        #This computes a date2num 1 minute step
        stepVal = dates.date2num(datetime(2000, 1, 1, hour=0, minute=1, second=0)) - dates.date2num(datetime(2000, 1, 1, hour=0, minute=0, second=0))
        
        self.sliderax = figure.add_axes([0.3, 0.05, 0.4, 0.04])
        self.slider = RangeSlider(self.sliderax, "Threshold", dates.date2num(self.df[timeColumn]).min(), dates.date2num(self.df[timeColumn]).max() - (2 * stepVal), valstep=stepVal * self.granularity, valinit=[dates.date2num(self.df[timeColumn]).min(), dates.date2num(self.df[timeColumn]).max()])
        
        i = 0
        print(self.df.columns)
        for column in self.df.columns:
            if column not in ['Datetime (UTC)', 'Datetime (Local)'] and self.numberOfGraphs > 1:
                print(column)
                self.axs[i].set_xlabel('Time (Hour:Min:Sec)')
                self.axs[i].set_ylabel(column)
                self.axs[i].xaxis.set_major_locator(plt.MaxNLocator(24))
                self.axs[i].tick_params(labelrotation=90)
                self.axs[i].margins(x=0.02, y=0.02)
                self.axs[i].grid(color='black', alpha=0.13)
                #self.axs[i].plot(self.df['Datetime (UTC)'], self.df[column], lw=2)                
                self.axs[i].plot(self.df[timeColumn].dt.strftime("%H:%M:%S"), self.df[column], lw=2)
                i += 1
                
            elif column not in ['Datetime (UTC)', 'Datetime (Local)']:
                print(column)
                self.axs.set_xlabel('Time (Hour:Min:Sec)')
                self.axs.set_ylabel(column)
                self.axs.xaxis.set_major_locator(plt.MaxNLocator(24))
                self.axs.tick_params(labelrotation=90)
                self.axs.margins(x=0.02, y=0.02)
                self.axs.grid(color='black', alpha=0.13)
                #self.axs.plot(self.df['Datetime (UTC)'], self.df[column], lw=2)                
                self.axs.plot(self.df[timeColumn].dt.strftime("%H:%M:%S"), self.df[column], lw=2)


        def update(val):
            i = 0
            lValRounded = dates.num2date(val[0])
            lValRounded = (lValRounded.replace(second=0, minute=lValRounded.minute, hour=lValRounded.hour) + timedelta(lValRounded.second // 30)).strftime("%H:%M:%S")
            rValRounded = dates.num2date(val[1])
            rValRounded = (rValRounded.replace(second=0, minute=rValRounded.minute, hour=rValRounded.hour) - timedelta(rValRounded.second // 30)).strftime("%H:%M:%S")            

            testerLim = self.df[self.df['Datetime (UTC)'].dt.strftime("%H:%M:%S") == lValRounded]

            #Protects from missing values
            if not testerLim.empty:
                leftLim = testerLim.index[0] + 1
            else:
                leftLim = False
                
            testerLim = self.df[self.df['Datetime (UTC)'].dt.strftime("%H:%M:%S") == rValRounded]

            #Protects from missing values
            if not testerLim.empty:
                rightLim = testerLim.index[0]
            else:
                rightLim = False

            for column in self.df.columns:
                if column != 'Datetime (UTC)' and self.numberOfGraphs > 1:
                    if leftLim and rightLim:
                        self.axs[i].set_xlim(left=leftLim, right=rightLim)
                    i += 1
                    
                elif column != 'Datetime (UTC)':
                    if leftLim and rightLim:
                        self.axs.set_xlim(left=leftLim, right=rightLim)

            
        self.slider.on_changed(update)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        canvas.draw()
        self.canvas = canvas


    def GetCanvas(self):
        return self.canvas


class VisualizerFrame(tk.Frame):
    """Responsible for displaying all plots and synchronizing callbacks in a frame"""

    def __init__(self, notebook, pathToFiles:str, chosenCols:list, timeColumn:str, patientId:str):
        """Creates a new visualization frame for displaying multiple time series plots"""
        super().__init__(notebook, highlightbackground="green", highlightthickness=2)
        self.summaryCsvPath = path.join(pathToFiles, SUMMARYFILENAME)
        self.metadataCsvPath = path.join(pathToFiles, METADATAFILENAME)
        self.dependentVariables = chosenCols[:]
        self.numOfGraphs = len(self.dependentVariables)

        self.label = tk.Label(self, text='Patient ID: ' + patientId)
        self.label.pack()
        
        self.graphManager = GraphManager(self, self.summaryCsvPath, chosenCols, timeColumn)
        self.graphManager.GetCanvas().get_tk_widget().pack(fill=tk.BOTH, expand=True)

		