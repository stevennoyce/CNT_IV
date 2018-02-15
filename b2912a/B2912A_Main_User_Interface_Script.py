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

## ********** Parameters **********

os.chdir(sys.path[0])

if platform.node() == 'noyce-dell':
	chipID = 'C127P'
	deviceID = '15-16'
else:
	chipID = 'C127Fake'
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
	'chipID':chipID,
	'deviceID':deviceID,
	'dataFolder':'data/',
	'plotsFolder':'CurrentPlots/',
	'postFigures':	True,
	'NPLC':1,
	'GateSweep':{
		'saveFileName': 'GateSweep',
		'runDataPoints': 600,
		'complianceCurrent':	100e-6,
		'drainVoltageSetPoint':	0.5,
		'gateVoltageMinimum':	-15.0,
		'gateVoltageMaximum':	15.0
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
		'numberOfSweeps': 24,
		'applyStaticBiasBetweenSweeps': True,
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
		'excludeDataBeforeJSONExperimentNumber': 0,
		'excludeDataAfterJSONExperimentNumber':  float('inf'),
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
		parameters['deviceDirectory'] = parameters['dataFolder'] + parameters['chipID'] + '/' + parameters['deviceID'] + '/'	

		print('Parameters: ')
		print_dict(parameters, 0)
		confirmation = str(input('Are parameters correct? (y/n): '))

		if(confirmation == 'y'):
			runAction(parameters)
		else:
			break

def runAction(parameters):
	dlu.makeFolder(parameters['deviceDirectory'])
	dlu.makeFolder(parameters['plotsFolder'])
	dlu.emptyFolder(parameters['plotsFolder'])
	
	if(parameters['runType'] not in ['DeviceHistory', 'ChipHistory']):
		dlu.incrementJSONExperiementNumber(parameters['deviceDirectory'])
		smu_instance = smu.getConnectionFromVisa(parameters['NPLC'], defaultComplianceCurrent=100e-6, smuTimeout=60000)
		#smu_instance = smu.getConnectionToPCB()
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
		raise NotImplementedError("Invalid action for the B2912A Source Measure Unit")
	
	if(parameters['runType'] not in ['DeviceHistory', 'ChipHistory']):
		smu_instance.rampDownVoltages()
		parameters['endIndexes'] = dlu.loadJSONIndex(parameters['deviceDirectory'])
		dlu.saveJSON(parameters['deviceDirectory'], 'ParametersHistory', parameters, incrementIndex=False)
		plotPoster.postPlots(parameters)
	




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

