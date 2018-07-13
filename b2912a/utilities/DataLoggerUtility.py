import os
import json
import glob



# === File System ===
def makeFolder(folderPath):
	if (not os.path.exists(folderPath)):
		os.makedirs(folderPath)

def emptyFolder(folderPath):
	if os.path.exists(folderPath):
		fileNames = glob.glob(folderPath + '*.png')
		for fileName in fileNames:
			os.remove(fileName)



# === JSON ===
def saveJSON(directory, saveFileName, jsonData, incrementIndex=True):
	with open(os.path.join(directory, saveFileName + '.json'), 'a') as file:
		if incrementIndex:
			indexData = loadJSONIndex(directory)
			jsonData['index'] = indexData['index']
			jsonData['experimentNumber'] = indexData['experimentNumber']
			incrementJSONIndex(directory)
		
		json.dump(jsonData, file)
		file.write('\n')

def loadJSON(directory, loadFileName):
	jsonData = []
	with open(os.path.join(directory, loadFileName)) as file:
		for line in file:
			try:
				jsonData.append(json.loads(str(line)))
			except:
				print('Error loading JSON line in file {:}/{:}'.format(directory, loadFileName))
	return jsonData

def loadJSONIndex(directory):
	indexData = {}
	try:
		with open(os.path.join(directory, 'index.json'), 'r') as file:
			indexData = json.loads(file.readline())
	except FileNotFoundError:	
		indexData = {'index':0, 'experimentNumber':0}

	return indexData

def incrementJSONIndex(directory):
	indexData = loadJSONIndex(directory)
	with open(os.path.join(directory, 'index.json'), 'w') as file:
		indexData['index'] += 1
		json.dump(indexData, file)
		file.write('\n')
	return indexData['index']

def incrementJSONExperiementNumber(directory):
	indexData = loadJSONIndex(directory)
	with open(os.path.join(directory, 'index.json'), 'w') as file:
		indexData['experimentNumber'] += 1
		json.dump(indexData, file)
		file.write('\n')
	return indexData['experimentNumber']

def loadIndexesOfExperiementRange(directory, startExperimentNumber, endExperimentNumber):
	indexes = []
	for fileName in glob.glob(directory + '/*.json'):
		if not os.path.basename(fileName) in ['BurnOut.json', 'GateSweep.json', 'StaticBias.json']:
			continue
		jsonData = loadJSON('', fileName)
		for deviceRun in jsonData:
			if (deviceRun['experimentNumber'] >= startExperimentNumber) and (deviceRun['experimentNumber'] <= endExperimentNumber):
				indexes.append(deviceRun['index'])
	indexes.sort()
	return indexes



# === Device History API ===
def getDeviceDirectory(parameters):
	return os.path.join(parameters['dataFolder'], parameters['waferID'], parameters['chipID'], parameters['deviceID']) + '/'

def loadFullDeviceHistory(directory, fileName, deviceID):
	return loadJSON(directory, fileName)
	#jsonData = loadJSON(directory, fileName)
	#deviceHistory = []
	#for deviceRun in jsonData:
	#	if(deviceRun['deviceID'] == deviceID):
	#		deviceHistory.append(deviceRun)
	#return deviceHistory

def loadSpecificDeviceHistory(directory, fileName, minIndex=0, maxIndex=float('inf'), minExperiment=0, maxExperiment=float('inf'), minRelativeIndex=0, maxRelativeIndex=float('inf')):
	filteredHistory = loadJSON(directory, fileName)

	if(minIndex > 0):
		filteredHistory = filterHistoryGreaterThan(filteredHistory, 'index', minIndex)
	if(maxIndex < float('inf')):
		filteredHistory = filterHistoryLessThan(filteredHistory, 'index', maxIndex)

	if(minExperiment > 0):
		filteredHistory = filterHistoryGreaterThan(filteredHistory, 'experimentNumber', minExperiment)
	if(maxExperiment < float('inf')):
		filteredHistory = filterHistoryLessThan(filteredHistory, 'experimentNumber', maxExperiment)

	if(minRelativeIndex > 0 or maxRelativeIndex < float('inf')):
		experimentBaseIndex = min(loadIndexesOfExperiementRange(directory, minExperiment, maxExperiment))
		if(minRelativeIndex > 0):
			filteredHistory = filterHistoryGreaterThan(filteredHistory, 'index', experimentBaseIndex + minRelativeIndex)
		if(maxRelativeIndex < float('inf')):
			filteredHistory = filterHistoryLessThan(filteredHistory, 'index', experimentBaseIndex + maxRelativeIndex)

	return filteredHistory

def loadFullChipHistory(directory, fileName, chipID):
	chipHistory = []
	for deviceSubdirectory in [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]:
		jsonData = loadJSON(directory + deviceSubdirectory + '/', fileName)
		for deviceRun in jsonData:
			if(deviceRun['chipID'] == chipID):
				chipHistory.append(deviceRun)
	return chipHistory



# === Chip History API ===
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



# === Filter ===
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

def filterHistoryBetween(deviceHistory, property, lower, upper):










	

