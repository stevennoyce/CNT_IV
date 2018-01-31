import os
import json
import glob

def makeFolder(folderPath):
	if (not os.path.exists(folderPath)):
		os.makedirs(folderPath)

def emptyFolder(folderPath):
	if os.path.exists(folderPath):
		fileNames = glob.glob('*.png')
		for fileName in fileNames:
			os.remove(fileName)

# ***** CSV *****

def initCSV(directory, saveFileName):
	with open(directory + saveFileName + '.csv', 'a') as file:
		file.write(' ')

def saveCSV(directory, saveFileName, csvData):
	with open(directory + saveFileName + '.csv', 'a') as file:
		line = str(csvData)[1:-1] + "\n"
		file.write(line)

# ***** JSON *****

def saveJSON(directory, saveFileName, jsonData, incrementIndex=True):
	with open(directory + saveFileName + '.json', 'a') as file:
		if incrementIndex:
			indexData = loadJSONIndex(directory)
			jsonData['index'] = indexData['index']
			jsonData['experimentNumber'] = indexData['experimentNumber']
			incrementJSONIndex(directory)
		
		json.dump(jsonData, file)
		file.write('\n')

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
	indexData = {}
	try:
		with open(directory + 'index.json', 'r') as file:
			indexData = json.loads(file.readline())
	except FileNotFoundError:	
		indexData = {'index':0, 'experimentNumber':0}

	return indexData

def incrementJSONIndex(directory):
	indexData = loadJSONIndex(directory)
	with open(directory + 'index.json', 'w') as file:
		indexData['index'] += 1
		json.dump(indexData, file)
		file.write('\n')

def incrementJSONExperiementNumber(directory):
	indexData = loadJSONIndex(directory)
	with open(directory + 'index.json', 'w') as file:
		indexData['experimentNumber'] += 1
		json.dump(indexData, file)
		file.write('\n')



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
		try:
			if(deviceRun[property] == value):
				filteredHistory.append(deviceRun)
		except:
			print("Unable to apply filter on '"+str(property)+"' == '"+str(value)+"'")
	return filteredHistory

def filterHistoryGreaterThan(deviceHistory, property, threshold):
	filteredHistory = []
	for deviceRun in deviceHistory:
		try:
			if(deviceRun[property] >= threshold):
				filteredHistory.append(deviceRun)
		except:
			print("Unable to apply filter on '"+str(property)+"' >= '"+str(value)+"'")
	return filteredHistory

def filterHistoryLessThan(deviceHistory, property, threshold):
	filteredHistory = []
	for deviceRun in deviceHistory:
		try:
			if(deviceRun[property] <= threshold):
				filteredHistory.append(deviceRun)
		except:
			print("Unable to apply filter on '"+str(property)+"' <= '"+str(value)+"'")
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



