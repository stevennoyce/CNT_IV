import os
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

## ********** Parameters **********

if platform.node() == 'noyce-dell':
	chipID = 'C127P'
	deviceID = '1-2'
else:
	chipID = 'C127E'
	deviceID = '15-16'

saveFolder = 'data/'

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
	'saveFolder':saveFolder,
	'figuresSaved':[],
	'postFigures':	True,
	'NPLC':1
}

additional_parameters = {
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
		'complianceCurrent':	2000e-6,
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
		'complianceCurrent':	100e-6,
		'startUpSettlingDelay': 2,
		'biasTime': 60*60,
		'gateVoltageSetPoint':	-15.0,
		'drainVoltageSetPoint':	1.0
	},
	'AutoGateSweep':{
		'numberOfSweeps': 24,
		'applyStaticBiasBetweenSweeps': True,
	},
	'AutoStaticBias':{
		'numberOfStaticBiases': 24,
		'applyGateSweepBetweenBiases': True,
		'delayBetweenBiases': 0,
		'numberOfBiasesBetweenIncrements': 4,
		'incrementStaticDrainVoltage': 0.2,
		'incrementStaticGateVoltage':  0
	},
	'DeviceHistory':{
		'plotGateSweeps': 	True,
		'plotBurnOuts': 	True,
		'plotStaticBias': 	True,
		'saveFiguresGenerated': False,
		'excludeDataBeforeJSONIndex': 0,
		'excludeDataAfterJSONIndex':  float('inf'),
		'excludeDataBeforeJSONExperimentNumber': 12,
		'excludeDataAfterJSONExperimentNumber':  17,
		'showOnlySuccessfulBurns': False
	},
	'ChipHistory':{

	}
}

def main(parameters):
	while(True):
		os.system('cls' if os.name == 'nt' else 'clear')
		print('Actions: ')
		print_dict(runTypes)
		choice = int(input('Choose an action (0,1,2,...): '))

		if(choice == 0):
			break

		parameters = {'runType': runTypes[choice]}
		parameters = {**parameters, **default_parameters}
		parameters = {**parameters, **additional_parameters[runTypes[choice]]}

		print('Parameters: ')
		print_dict(parameters)
		confirmation = str(input('Are parameters correct? (y/n): '))

		if(confirmation == 'y'):
			runAction(parameters)
		else:
			break
		
def runAction(parameters):
	parameters['deviceDirectory'] = parameters['saveFolder'] + parameters['chipID'] + '/' + parameters['deviceID'] + '/'
	
	if(parameters['runType'] not in ['DeviceHistory', 'ChipHistory']):
		parameters['deviceDirectory'] = parameters['saveFolder'] + parameters['chipID'] + '/' + parameters['deviceID'] + '/'
		dlu.makeFolder(parameters['deviceDirectory'])
		dlu.incrementJSONExperiementNumber(parameters['deviceDirectory'])
	
	parameters['startIndexes'] = dlu.loadJSONIndex(parameters['deviceDirectory'])
	
	if(parameters['runType'] == 'GateSweep'):
		gateSweepScript.run(parameters)
	elif(parameters['runType'] == 'BurnOut'):
		burnOutScript.run(parameters)
	elif(parameters['runType'] == 'AutoBurnOut'):
		parameters['GateSweep'] = additional_parameters['GateSweep']
		parameters['BurnOut'] = additional_parameters['BurnOut']
		autoBurnScript.run(parameters)
	elif(parameters['runType'] == 'StaticBias'):
		staticBiasScript.run(parameters)
	elif(parameters['runType'] == 'AutoGateSweep'):
		parameters['GateSweep'] = additional_parameters['GateSweep']
		parameters['StaticBias'] = additional_parameters['StaticBias']
		autoGateScript.run(parameters)
	elif(parameters['runType'] == 'AutoStaticBias'):
		parameters['GateSweep'] = additional_parameters['GateSweep']
		parameters['StaticBias'] = additional_parameters['StaticBias']
		autoBiasScript.run(parameters)
	elif(parameters['runType'] == 'DeviceHistory'):
		deviceHistoryScript.run(parameters)
	elif(parameters['runType'] == 'ChipHistory'):
		chipHistoryScript.run(parameters)
	else:
		raise NotImplementedError("Invalid action for the B2912A Source Measure Unit")
	
	parameters['endIndexes'] = dlu.loadJSONIndex(parameters['deviceDirectory'])
	plotPoster.postPlots(parameters)




def print_dict(dict):
	keys = list(dict.keys())
	for i in range(len(keys)):
		print('  ' + str(keys[i]) + ': ' + str(dict[keys[i]]))


if __name__ == '__main__':
    main(default_parameters)

