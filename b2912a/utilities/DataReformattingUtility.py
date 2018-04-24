import glob
import os

import DataLoggerUtility as dlu

directory = '../data/C127P/'

gateSweepFileName = 'GateSweep.json'
burnOutFileName = 'BurnOut.json'
staticBiasFileName = 'StaticBias.json'

default_parameters = {
	'ParametersFormatVersion': 2,
	'GateSweep':{
		'saveFileName': 'GateSweep',
		'isFastSweep': False,
		'isAlternatingSweep': False,
		'pulsedMeasurementOnTime': 0,
		'pulsedMeasurementOffTime': 0,
		'stepsInVGSPerDirection': 100,
		'pointsPerVGS': 1,
		'complianceCurrent':	100e-6,
		'drainVoltageSetPoint':	-0.5,
		'gateVoltageMinimum':	-3.5,
		'gateVoltageMaximum': 	3.5
	},
	'BurnOut':{
		'saveFileName': 'BurnOut',
		'pointsPerRamp': 50,
		'pointsPerHold': 50,
		'complianceCurrent':	2e-3,
		'thresholdProportion':	0.8,
		'minimumAppliedDrainVoltage': 0,
		'gateVoltageSetPoint':	15.0,
		'drainVoltageMaxPoint':	10,
		'drainVoltagePlateaus': 10
	},
	'AutoBurnOut':{
		'targetOnOffRatio': 300,
		'limitBurnOutsAllowed': 8,
		'limitOnOffRatioDegradation': 0.7
	},
	'StaticBias':{
		'saveFileName': 'StaticBias',
		'totalBiasTime': 60*60,
		'measurementTime': 10,
		'complianceCurrent': 100e-6,
		'delayBeforeApplyingVoltage': 0,
		'delayBeforeMeasurementsBegin': 0,
		'gateVoltageSetPoint': 	-15,
		'drainVoltageSetPoint':	-0.5,
		'gateVoltageWhenDone':  0,
		'drainVoltageWhenDone': 0
	},
	'AutoGateSweep':{
		'numberOfSweeps': 3,
		'applyStaticBiasBetweenSweeps': False,
	},
	'AutoStaticBias':{
		'numberOfStaticBiases': 2,
		'applyGateSweepBetweenBiases': True,
		'firstDelayBeforeMeasurementsBegin': 0,
		'numberOfBiasesBetweenIncrements': 1,
		'incrementStaticGateVoltage': 0,
		'incrementStaticDrainVoltage': 0,
		'incrementGateVoltageWhenDone': 0,
		'incrementDrainVoltageWhenDone': 0,
		'incrementDelayBeforeReapplyingVoltage': 0,
		'shuffleDelaysBeforeReapplyingVoltage': False
	},
	'DeviceHistory':{
		'showFiguresGenerated': True,
		'saveFiguresGenerated': True,
		'postFiguresGenerated': False,
		'plotGateSweeps': True,
		'plotBurnOuts':   True,
		'plotStaticBias': True,
		'excludeDataBeforeJSONIndex': 0,
		'excludeDataAfterJSONIndex':  float('inf'),
		'excludeDataBeforeJSONExperimentNumber': 0,
		'excludeDataAfterJSONExperimentNumber':  float('inf'),
		'gateSweepDirection': ['both','forward','reverse'][0],
		'showOnlySuccessfulBurns': False,
		'timescale': ['','seconds','minutes','hours','days','weeks'][0],
		'plotInRealTime': True,
		'includeBiasVoltageSubplot': False
	},
	'ChipHistory':{
		
	},
	'Results':{

	},
	'SensorData':{

	},
	'MeasurementSystem':['B2912A','PCB2v14'][0],
	'deviceRange':[],#devicesInRange(2,32,skip=False),
	'dataFolder':'data/',
	'plotsFolder':'CurrentPlots/',
	'postFigures':	True,
	'NPLC':1
}

def main():
	for deviceSubdirectory in [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]:
		deviceDirectory = directory + deviceSubdirectory + '/'

		gateSweepHistory = dlu.loadJSON(deviceDirectory, gateSweepFileName)
		try:
			burnOutHistory = dlu.loadJSON(deviceDirectory, burnOutFileName)
			burnedout = True
		except:
			print('Device: ' + deviceSubdirectory + ' no burn-out')
			burnedout = False
		try:
			staticBiasHistory = dlu.loadJSON(deviceDirectory, staticBiasFileName)
			staticed = True
		except:
			print('Device: ' + deviceSubdirectory + ' no static bias')
			staticed = False
		index_json = dlu.loadJSON(deviceDirectory, 'index.json')[0]

		if('ParametersFormatVersion' in gateSweepHistory[0]):
			continue

		if os.path.exists(deviceDirectory):
			fileNames = glob.glob(deviceDirectory + '*')
			for fileName in fileNames:
				os.remove(fileName)

		for deviceRun in gateSweepHistory:
			if('ParametersFormatVersion' in deviceRun):
				continue

			if(not isinstance(deviceRun['voltage1s'][0], list)):
				length = len(deviceRun['voltage1s'])
				deviceRun['current1s'] = [deviceRun['current1s'][0:int(length/2)], deviceRun['current1s'][int(length/2):]]
				deviceRun['current2s'] = [deviceRun['current2s'][0:int(length/2)], deviceRun['current2s'][int(length/2):]]
				deviceRun['voltage1s'] = [deviceRun['voltage1s'][0:int(length/2)], deviceRun['voltage1s'][int(length/2):]]
				deviceRun['voltage2s'] = [deviceRun['voltage2s'][0:int(length/2)], deviceRun['voltage2s'][int(length/2):]]	
				deviceRun['timestamps'] = [deviceRun['timestamps'][0:int(length/2)], deviceRun['timestamps'][int(length/2):]]	
				deviceRun['gateVoltages'] = [deviceRun['gateVoltages'][0:int(length/2)], deviceRun['gateVoltages'][int(length/2):]]	

			if('figuresSaved' in deviceRun):
				del deviceRun['figuresSaved']

			if('MeasurementSystem' not in deviceRun):
				deviceRun['MeasurementSystem'] = 'B2912A'

			if('deviceRange' not in deviceRun):
				deviceRun['deviceRange'] = []

			if('plotsFolder' not in deviceRun):
				deviceRun['plotsFolder'] = 'CurrentPlots/'

			if('deviceDirectory' not in deviceRun):
				deviceRun['deviceDirectory'] = deviceDirectory[3:]

			if('ParametersFormatVersion' not in deviceRun):
				deviceRun['ParametersFormatVersion'] = 1.1

			if('startIndexes' not in deviceRun):
				deviceRun['startIndexes'] = {'index':deviceRun['index'], 'experimentNumber':deviceRun['experimentNumber']}

			if('gateVoltageMinimum' in deviceRun):
				deviceRun['GateSweep'] = dict(default_parameters['GateSweep'])
				deviceRun['GateSweep']['complianceCurrent'] = deviceRun['complianceCurrent']
				deviceRun['GateSweep']['drainVoltageSetPoint'] = deviceRun['drainVoltageSetPoint']
				deviceRun['GateSweep']['gateVoltageMinimum'] = deviceRun['gateVoltageMinimum']
				deviceRun['GateSweep']['gateVoltageMaximum'] = deviceRun['gateVoltageMaximum']
				deviceRun['GateSweep']['pointsPerVGS'] = count(deviceRun['gateVoltages'][0])
				deviceRun['GateSweep']['stepsInVGSPerDirection'] = int(deviceRun['runDataPoints']/(2*deviceRun['GateSweep']['pointsPerVGS']))
				del deviceRun['drainVoltageSetPoint']
				del deviceRun['gateVoltageMinimum']
				del deviceRun['gateVoltageMaximum']
				del deviceRun['runDataPoints']
				del deviceRun['complianceCurrent']
				del deviceRun['saveFileName']

			if('BurnOut' in deviceRun and ('runDataPoints' in deviceRun['BurnOut'])):
				deviceRun['BurnOut']['pointsPerRamp'] = 50
				deviceRun['BurnOut']['pointsPerHold'] = 50
				del deviceRun['BurnOut']['runDataPoints']

			if('targetOnOffRatio' in deviceRun):
				deviceRun['AutoBurnOut'] = dict(default_parameters['AutoBurnOut'])
				deviceRun['AutoBurnOut']['targetOnOffRatio'] = deviceRun['targetOnOffRatio']
				deviceRun['AutoBurnOut']['limitBurnOutsAllowed'] = deviceRun['limitBurnOutsAllowed']
				deviceRun['AutoBurnOut']['limitOnOffRatioDegradation'] = deviceRun['limitOnOffRatioDegradation']
				del deviceRun['targetOnOffRatio']
				del deviceRun['limitBurnOutsAllowed']
				del deviceRun['limitOnOffRatioDegradation']

			if('numberOfStaticBiases' in deviceRun):
				deviceRun['AutoStaticBias'] = dict(default_parameters['AutoStaticBias'])
				deviceRun['AutoStaticBias']['numberOfStaticBiases'] = deviceRun['numberOfStaticBiases']
				deviceRun['AutoStaticBias']['applyGateSweepBetweenBiases'] = deviceRun['applyGateSweepBetweenBiases']
				deviceRun['AutoStaticBias']['numberOfBiasesBetweenIncrements'] = deviceRun['numberOfBiasesBetweenIncrements']
				deviceRun['AutoStaticBias']['incrementStaticDrainVoltage'] = deviceRun['incrementStaticDrainVoltage']
				deviceRun['AutoStaticBias']['incrementStaticGateVoltage'] = deviceRun['incrementStaticGateVoltage']
				del deviceRun['numberOfStaticBiases']
				del deviceRun['applyGateSweepBetweenBiases']
				del deviceRun['numberOfBiasesBetweenIncrements']
				del deviceRun['incrementStaticDrainVoltage']
				del deviceRun['incrementStaticGateVoltage']

		if(burnedout):
			for deviceRun in burnOutHistory:
				if('ParametersFormatVersion' in deviceRun):
					continue

				if('figuresSaved' in deviceRun):
					del deviceRun['figuresSaved']

				if('MeasurementSystem' not in deviceRun):
					deviceRun['MeasurementSystem'] = 'B2912A'

				if('deviceRange' not in deviceRun):
					deviceRun['deviceRange'] = []

				if('plotsFolder' not in deviceRun):
					deviceRun['plotsFolder'] = 'CurrentPlots/'

				if('deviceDirectory' not in deviceRun):
					deviceRun['deviceDirectory'] = deviceDirectory[3:]

				if('ParametersFormatVersion' not in deviceRun):
					deviceRun['ParametersFormatVersion'] = 1.1

				if('startIndexes' not in deviceRun):
					deviceRun['startIndexes'] = {'index':deviceRun['index'], 'experimentNumber':deviceRun['experimentNumber']}

				if('targetOnOffRatio' in deviceRun):
					deviceRun['AutoBurnOut'] = dict(default_parameters['AutoBurnOut'])
					deviceRun['AutoBurnOut']['targetOnOffRatio'] = deviceRun['targetOnOffRatio']
					deviceRun['AutoBurnOut']['limitBurnOutsAllowed'] = deviceRun['limitBurnOutsAllowed']
					deviceRun['AutoBurnOut']['limitOnOffRatioDegradation'] = deviceRun['limitOnOffRatioDegradation']
					del deviceRun['targetOnOffRatio']
					del deviceRun['limitBurnOutsAllowed']
					del deviceRun['limitOnOffRatioDegradation']

				if('runDataPoints' in deviceRun):
					deviceRun['BurnOut'] = dict(default_parameters['BurnOut'])
					deviceRun['BurnOut']['thresholdProportion'] = deviceRun['thresholdProportion']
					deviceRun['BurnOut']['minimumAppliedDrainVoltage'] = deviceRun['minimumAppliedDrainVoltage']
					deviceRun['BurnOut']['complianceCurrent'] = deviceRun['complianceCurrent']
					deviceRun['BurnOut']['gateVoltageSetPoint'] = deviceRun['gateVoltageSetPoint']
					deviceRun['BurnOut']['drainVoltageMaxPoint'] = deviceRun['drainVoltageMaxPoint']
					deviceRun['BurnOut']['drainVoltagePlateaus'] = deviceRun['drainVoltagePlateaus']
					del deviceRun['thresholdProportion']
					del deviceRun['saveFileName']
					del deviceRun['runDataPoints']
					del deviceRun['complianceCurrent']
					del deviceRun['minimumAppliedDrainVoltage']
					del deviceRun['gateVoltageSetPoint']
					del deviceRun['drainVoltageMaxPoint']
					del deviceRun['drainVoltagePlateaus']
				
		if(staticed):			
			for deviceRun in staticBiasHistory:
				if('ParametersFormatVersion' in deviceRun):
					continue

				if('figuresSaved' in deviceRun):
					del deviceRun['figuresSaved']

				if('MeasurementSystem' not in deviceRun):
					deviceRun['MeasurementSystem'] = 'B2912A'

				if('deviceRange' not in deviceRun):
					deviceRun['deviceRange'] = []

				if('plotsFolder' not in deviceRun):
					deviceRun['plotsFolder'] = 'CurrentPlots/'

				if('deviceDirectory' not in deviceRun):
					deviceRun['deviceDirectory'] = deviceDirectory[3:]

				if('ParametersFormatVersion' not in deviceRun):
					deviceRun['ParametersFormatVersion'] = 1.1

				if('startIndexes' not in deviceRun):
					deviceRun['startIndexes'] = {'index':deviceRun['index'], 'experimentNumber':deviceRun['experimentNumber']}

				if('numberOfStaticBiases' in deviceRun):
					deviceRun['AutoStaticBias'] = dict(default_parameters['AutoStaticBias'])
					deviceRun['AutoStaticBias']['numberOfStaticBiases'] = deviceRun['numberOfStaticBiases']
					deviceRun['AutoStaticBias']['applyGateSweepBetweenBiases'] = deviceRun['applyGateSweepBetweenBiases']
					deviceRun['AutoStaticBias']['numberOfBiasesBetweenIncrements'] = deviceRun['numberOfBiasesBetweenIncrements']
					deviceRun['AutoStaticBias']['incrementStaticDrainVoltage'] = deviceRun['incrementStaticDrainVoltage']
					deviceRun['AutoStaticBias']['incrementStaticGateVoltage'] = deviceRun['incrementStaticGateVoltage']
					del deviceRun['numberOfStaticBiases']
					del deviceRun['applyGateSweepBetweenBiases']
					del deviceRun['numberOfBiasesBetweenIncrements']
					del deviceRun['incrementStaticDrainVoltage']
					del deviceRun['incrementStaticGateVoltage']

		for deviceRun in gateSweepHistory:
			dlu.saveJSON(deviceDirectory, 'GateSweep', deviceRun, incrementIndex=False)
		if(burnedout):
			for deviceRun in burnOutHistory:
				dlu.saveJSON(deviceDirectory, 'BurnOut', deviceRun, incrementIndex=False)
		if(staticed):
			for deviceRun in staticBiasHistory:
				dlu.saveJSON(deviceDirectory, 'StaticBias', deviceRun, incrementIndex=False)
		dlu.saveJSON(deviceDirectory, 'index', index_json, incrementIndex=False)

def count(array):
	count = 1
	index = 1
	while(array[0] == array[index]):
		count += 1
		index += 1
	return count

main()

