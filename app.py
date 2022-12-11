""" 
App.py:
    This is the main Python script to run the application.
    This file should only contain glue code at top level, or temporary development glue code.
"""

from tkinter import *
from src.Window import Window
from src.Utils.Constants import DEFAULTPATHTODATASETS, APPNAME
import sys
import matplotlib
matplotlib.use('tkagg')

APPNAME='Digi-Vis'
APPVERSION = '1.0.0'
APPTITLE=APPNAME + ' ' + APPVERSION
DEFAULTPATHTODATASETS = './datasets'

def OnClose():
    """OnClose Function to fully quit the process, freeing up any memory"""
    sys.exit(0)

if __name__ == "__main__":
    window = Window(APPTITLE, DEFAULTPATHTODATASETS)
    window.protocol('WM_DELETE_WINDOW', OnClose)
    window.mainloop()
