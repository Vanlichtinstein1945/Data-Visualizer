import pandas as pd
from .Constants import TIME_SERIES_COLUMNS

"""Revisit this class after prototype"""
class DataFrame_Windowed():
	def __init__(self, filePath, colsToKeep=None):
		"""Initialize a windowed dataframe"""
		if colsToKeep:
			if 'Datetime (UTC)' not in colsToKeep:
				colsToKeep.append('Datetime (UTC)')
			if 'Timezone (minutes)' not in colsToKeep:
				colsToKeep.append('Timezone (minutes)')
			self.data = pd.read_csv(filePath, usecols=colsToKeep)
		else:
			self.data = pd.read_csv(filePath)
		
		self.timeZone = self.data.loc[0].at['Timezone (minutes)']
		print(self.data.head())
		self.data.drop(columns='Timezone (minutes)', inplace=True)
		print(self.data.head())
		print(self.data.columns)
		self.data['Datetime (Local)'] = pd.to_datetime(self.data['Datetime (UTC)']) + pd.DateOffset(minutes = int(self.timeZone))
		self.data['Datetime (Local)'] = self.data['Datetime (Local)'].dt.strftime('%H:%M:%S')

		self.data['Datetime (UTC)'] = pd.to_datetime(self.data['Datetime (UTC)'])
		self.data['Datetime (UTC)'] = self.data['Datetime (UTC)'].dt.strftime('%H:%M:%S')

		self.data.sort_values(by=['Datetime (UTC)'], inplace=True)
		self.filePath = filePath
		self.startDate_min = self.data['Datetime (UTC)'].min()
		self.endDate_max = self.data['Datetime (UTC)'].max()
		self.curStartDate = self.startDate_min
		self.curEndDate = self.endDate_max
		
		
	def RemoveColumn(self, colToDrop):
		if colToDrop == 'Datetime (UTC)':
			raise Exception('Cannot remove Datetime column from data frame. Required for Time Series.')

		try:
			self.data.drop(colToDrop, inplace=True, axis=1)
		except KeyError:
			print('Column ' + colToDrop + ' not found in dataframe.')


	def AddColumn(self, colToAdd):
		colToAddDF = pd.read_csv(self.filePath, usecols=[colToAdd, 'Datetime (UTC)'])
		self.data[colToAdd] = colToAddDF[colToAdd]


	def UpdateTimeWindows(self, startDate, endDate):
		"""Update the start and end date of the data frame. Note this does not update views"""
		self.curStartDate = startDate
		self.curEndDate = endDate


	def GetDataFrame(self):
		"""Returns view of data frame between the set """
		return self.data.loc[(self.data['Datetime (UTC)'] >= self.curStartDate) | (self.data['Datetime (UTC)'] <= self.curEndDate)]


	def GetSelectedColumns(self):
		"""Returns a list of selected columns excluding Datetime"""
		result = []
		for col in self.data.columns:
			if col not in ['Datetime (UTC)', 'Datetime (Local)']:
				result.append(col)
		return result


	def Aggregate(self):
		summaryStats = self.data.describe()
		summaryStats = summaryStats[[col for col in self.data.columns if col in TIME_SERIES_COLUMNS]]
		return summaryStats
		