import pandas as pd
import logging
import sys
from pathlib import Path

"""Revisit this class after prototype"""

#Might be a better way to do this - this was more or less how I was taught
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from src.Utils.DataFrame_Windowed import DataFrame_Windowed


#Initialize object
dfWin = DataFrame_Windowed('summary.csv',colsToKeep=['Datetime (UTC)', 'Timezone (minutes)', 'Unix Timestamp (UTC)',
       'Acc magnitude avg', 'Eda avg', 'Temp avg', 'Movement intensity',
       'Steps count', 'Rest', 'On Wrist'])


#Aggregate function check
print("Summary stats: ", dfWin.Aggregate(), "\n\n")

#Time window check
testMin = pd.to_datetime(dfWin.data['Datetime'].min() + pd.Timedelta(days=1))
testMax = pd.to_datetime(dfWin.data['Datetime'].max())
print("Before updating time window: ", dfWin.data.head(), "\n\n")
dfWin.UpdateTimeWindows(testMin, testMax)
print("After updating time window: ", dfWin.data.head(), "\n\n")

#Column Add/remove check
print("Columns before removal: ", dfWin.data.columns, "\n\n")
dfWin.RemoveColumn('Steps count')
print("Columns after removal: ", dfWin.data.columns, "\n\n")
dfWin.AddColumn('Steps count')
print("Columns after adding column back: ", dfWin.data.columns, "\n\n")
