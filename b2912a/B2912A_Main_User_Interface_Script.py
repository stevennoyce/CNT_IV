import os
import sys
import platform

import B2912A_Burn_Out as burnOutScript
import B2912A_Gate_Sweep as gateSweepScript
import B2912A_Auto_Burn_Out as autoBurnScript
import B2912A_Static_Bias as staticBiasScript
import B2912A_Auto_Gate_Sweep as autoGateScript
import B2912A_Auto_Static_Bias as autoBiasScript
import Device_History as deviceHistoryScript
import Chip_History as chipHistoryScript

from utilities import DataLoggerUtility as dlu
from utilities import PlotPostingUtility as plotPoster
from framework import SourceMeasureUnit as smu

def devicesInRange(startContact, endContact, skip=True):
	contactList = set(range(startContact,endContact))
	if(skip):
		omitList = set(range(4,64+1,4))
		contactList = list(contactList-omitList)
	return ['{0:}-{1:}'.format(c, c+1) for c in contactList]

## ********** Parameters **********

os.chdir(sys.path[0])

if platform.node() == 'noyce-dell':
	chipID = 'C127P'
	deviceID = '15-16'
else:
	chipID = 'C131H'
	deviceID = '1-2'

runTypes = {
	0:'Quit',
	1:'GateSweep',
	2:'BurnOut',
	3:'AutoBurnOut',
	4:'StaticBias',
	5:'AutoGateSweep',
	6:'AutoStaticBias',
	7:'DeviceHistory',
	8:'ChipHistory'
}

default_parameters = {
	'MeasurementSystem':['B2912A','PCB2v14'][1],
	'chipID':chipID,
	'deviceID':deviceID,
	'deviceRange':devicesInRange(1,32,skip=False),
	'dataFolder':'data/',
	'plotsFolder':'CurrentPlots/',
	'postFigures':	True,
	'NPLC':1,
	'GateSweep':{
		'saveFileName': 'GateSweep',
		'runFastSweep': False,
		'runDataPoints': 120,
		'pointsPerVGS': 1,
		'complianceCurrent':	100e-6,
		'drainVoltageSetPoint':	0.5,
		'gateVoltageMinimum':	-3.5,
		'gateVoltageMaximum':	3.5
	},
	'BurnOut':{
		'saveFileName': 'BurnOut',
		'runDataPoints': 1000,
		'complianceCurrent':	2e-3,
		'thresholdProportion':	0.8,
		'minimumAppliedDrainVoltage': 0.9,
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
		'runDataPoints': 60*6,
		'complianceCurrent': 100e-6,
		'delayBeforeApplyingVoltage': 30,
		'delayBeforeMeasurementsBegin': 0,
		'biasTime': 60*60,
		'gateVoltageSetPoint': 	-15.0,
		'drainVoltageSetPoint':	  1.0,
		'gateVoltageWhenDone':  -15.0,
		'drainVoltageWhenDone':  1.0
	},
	'AutoGateSweep':{
		'numberOfSweeps': 1,
		'applyStaticBiasBetweenSweeps': False,
	},
	'AutoStaticBias':{
		'numberOfStaticBiases': 12,
		'applyGateSweepBetweenBiases': False,
		'firstDelayBeforeMeasurementsBegin': 60*60*6,
		'numberOfBiasesBetweenIncrements': 1,
		'incrementStaticGateVoltage':  0,
		'incrementStaticDrainVoltage': 0,
		'incrementGateVoltageWhenDone': 2,
		'incrementDrainVoltageWhenDone': 0,
		'incrementDelayBeforeReapplyingVoltage': 0,
		'shuffleDelaysBeforeReapplyingVoltage': False
	},
	'DeviceHistory':{
		'saveFiguresGenerated': True,
		'plotGateSweeps': True,
		'plotBurnOuts':   True,
		'plotStaticBias': True,
		'excludeDataBeforeJSONIndex': 0,
		'excludeDataAfterJSONIndex':  float('inf'),
		'excludeDataBeforeJSONExperimentNumber': 13,
		'excludeDataAfterJSONExperimentNumber':  13,
		'gateSweepDirection': ['both','forward','reverse'][0],
		'showOnlySuccessfulBurns': False,
		'timescale': ['seconds','minutes','hours','days','weeks'][3],
		'plotInRealTime': True
	},
	'ChipHistory':{

	}
}

def main(parameters):
	while(True):
		os.system('cls' if os.name == 'nt' else 'clear')
		print('Actions: ')
		print_dict(runTypes, 0)
		choice = int(input('Choose an action (0,1,2,...): '))

		if(choice == 0):
			break

		parameters = dict(default_parameters)
		parameters['runType'] = runTypes[choice]

		print('Parameters: ')
		print_dict(parameters, 0)
		confirmation = str(input('Are parameters correct? (y/n): '))
		if(confirmation != 'y'):
			break
		
		smu_instance = None
		if(parameters['runType'] not in ['DeviceHistory', 'ChipHistory']):
			if(parameters['MeasurementSystem'] == 'B2912A'):
				smu_instance = smu.getConnectionFromVisa(parameters['NPLC'], defaultComplianceCurrent=100e-6, smuTimeout=60000)
			elif(parameters['MeasurementSystem'] == 'PCB2v14'):
				smu_instance = smu.getConnectionToPCB()
			else:
				raise NotImplementedError("Unkown Measurement System specified (try B2912A, PCB2v14, etc)")

		if((parameters['MeasurementSystem'] == 'PCB2v14') and (len(parameters['deviceRange']) > 0)):
			for device in parameters['deviceRange']:
				parameters = dict(default_parameters)
				parameters['runType'] = runTypes[choice]
				parameters['deviceID'] = device
				runAction(parameters, smu_instance)
		else:
			runAction(parameters, smu_instance)

def runAction(parameters, smu_instance):
	parameters['deviceDirectory'] = parameters['dataFolder'] + parameters['chipID'] + '/' + parameters['deviceID'] + '/'	
	dlu.makeFolder(parameters['deviceDirectory'])
	dlu.makeFolder(parameters['plotsFolder'])
	dlu.emptyFolder(parameters['plotsFolder'])
	
	if(parameters['runType'] not in ['DeviceHistory', 'ChipHistory']):
		dlu.incrementJSONExperiementNumber(parameters['deviceDirectory'])
		smu_instance.setDevice(parameters['deviceID'])
		parameters['startIndexes'] = dlu.loadJSONIndex(parameters['deviceDirectory'])	

	if(parameters['runType'] == 'GateSweep'):
		gateSweepScript.run(parameters, smu_instance)
	elif(parameters['runType'] == 'BurnOut'):
		burnOutScript.run(parameters, smu_instance)
	elif(parameters['runType'] == 'AutoBurnOut'):
		autoBurnScript.run(parameters, smu_instance)
	elif(parameters['runType'] == 'StaticBias'):
		staticBiasScript.run(parameters, smu_instance)
	elif(parameters['runType'] == 'AutoGateSweep'):
		autoGateScript.run(parameters, smu_instance)
	elif(parameters['runType'] == 'AutoStaticBias'):
		autoBiasScript.run(parameters, smu_instance)
	elif(parameters['runType'] == 'DeviceHistory'):
		deviceHistoryScript.run(parameters)
	elif(parameters['runType'] == 'ChipHistory'):
		chipHistoryScript.run(parameters)
	else:
		raise NotImplementedError("Invalid action for the Source Measure Unit")
	
	if(parameters['runType'] not in ['DeviceHistory', 'ChipHistory']):
		smu_instance.rampDownVoltages()
		parameters['endIndexes'] = dlu.loadJSONIndex(parameters['deviceDirectory'])
		dlu.saveJSON(parameters['deviceDirectory'], 'ParametersHistory', parameters, incrementIndex=False)
		plotPoster.postPlots(parameters)
	


# *** Helper Functions ***

def print_dict(dictionary, numtabs):
	keys = list(dictionary.keys())
	for i in range(len(keys)):
		if(isinstance(dictionary[keys[i]], dict)):
			print(" '" + str(keys[i])+ "': {")
			print_dict(dictionary[keys[i]], numtabs+1)
		else:
			print(numtabs*'\t'+'  ' + str(keys[i]) + ': ' + str(dictionary[keys[i]]))




if __name__ == '__main__':
    main(default_parameters)

