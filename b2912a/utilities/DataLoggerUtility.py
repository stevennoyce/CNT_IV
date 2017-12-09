import os
import json

def makeFolder(folderPath):
	if (not os.path.exists(folderPath)):
		os.makedirs(folderPath)

# ***** CSV *****

def initCSV(directory, saveFileName):
	with open(directory + saveFileName + '.csv', 'a') as file:
		file.write(' ')

def saveCSV(directory, saveFileName, csvData):
	with open(directory + saveFileName + '.csv', 'a') as file:
		line = str(csvData)[1:-1] + "\n"
		file.write(line)

# ***** JSON *****

def saveJSON(directory, saveFileName, jsonData):
	with open(directory + saveFileName + '.json', 'a') as file:
		jsonData['index'] = loadJSONIndex(directory)
		json.dump(jsonData, file)
		file.write('\r\n')

def loadJSON(directory, loadFileName):
	jsonData = []
	with open(directory + loadFileName) as file:
		for line in file:
			try:
				jsonData.append(json.loads(str(line)))
			except:
				print('Error loading JSON line')
	return jsonData

def loadJSONIndex(directory):
	index = 0
	indexData = {}
	try:
		with open(directory + 'index.json', 'r') as file:
			indexData = json.loads(file.readline())
			index = indexData['index'] + 1
			indexData['index'] = index
	except FileNotFoundError:	
		indexData = {'index':0}

	with open(directory + 'index.json', 'w') as file:
		json.dump(indexData, file)
		file.write('\r\n')
	return index

def loadFullDeviceHistory(directory, fileName, deviceID):
	jsonData = loadJSON(directory, fileName)
	deviceHistory = []
	for deviceRun in jsonData:
		if(deviceRun['deviceID'] == deviceID):
			deviceHistory.append(deviceRun)
	return deviceHistory

def loadFullChipHistory(directory, fileName, chipID):
	chipHistory = []
	for deviceSubdirectory in [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]:
		jsonData = loadJSON(directory + deviceSubdirectory + '/', fileName)
		for deviceRun in jsonData:
			if(deviceRun['chipID'] == chipID):
				chipHistory.append(deviceRun)
	return chipHistory

def filterHistory(deviceHistory, property, value):
	filteredHistory = []
	for deviceRun in deviceHistory:
		if(deviceRun[property] == value):
			filteredHistory.append(deviceRun)
	return filteredHistory

def filterHistoryGreaterThan(deviceHistory, property, threshold):
	filteredHistory = []
	for deviceRun in deviceHistory:
		if(deviceRun[property] >= threshold):
			filteredHistory.append(deviceRun)
	return filteredHistory

def filterHistoryLessThan(deviceHistory, property, threshold):
	filteredHistory = []
	for deviceRun in deviceHistory:
		if(deviceRun[property] <= threshold):
			filteredHistory.append(deviceRun)
	return filteredHistory

def loadFirstRunChipHistory(directory, fileName, chipID):
	fullChipHistory = loadFullChipHistory(directory, fileName, chipID)
	firstRunsOnly = []
	devicesLogged = []
	for i in range(len(fullChipHistory)):
		deviceRun = fullChipHistory[i]
		if(deviceRun['deviceID'] not in devicesLogged):
			firstRunsOnly.append(deviceRun)
			devicesLogged.append(deviceRun['deviceID'])
	return firstRunsOnly

def loadMostRecentRunChipHistory(directory, fileName, chipID):
	fullChipHistory = list(reversed(loadFullChipHistory(directory, fileName, chipID)))
	lastRunsOnly = []
	devicesLogged = []
	for i in range(len(fullChipHistory)):
		deviceRun = fullChipHistory[i]
		if(deviceRun['deviceID'] not in devicesLogged):
			lastRunsOnly.append(deviceRun)
			devicesLogged.append(deviceRun['deviceID'])
	return lastRunsOnly



