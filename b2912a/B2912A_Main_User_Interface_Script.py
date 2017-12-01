import os

import B2912A_Burn_Out as burnOutScript
import B2912A_Gate_Sweep as gateSweepScript
import B2912A_Auto_Burn_Out as autoBurnScript
import B2912A_Static_Bias as staticBiasScript
import B2912A_Auto_Gate_Sweep as autoGateScript
import Device_History as deviceHistoryScript
import Chip_History as chipHistoryScript

## ********** Parameters **********

chipID = 'C127M'
deviceID = '23-24'

#saveFolder = '/Users/stevennoyce/Documents/home/Research/illumina/PSoC/Layout 2_14/Version 2/Host/Testing/'
saveFolder = '/Users/jaydoherty/Documents/myWorkspaces/Python/Research/CNT_IV/b2912a/data/'

runTypes = {
	0:'Quit',
	1:'GateSweep',
	2:'BurnOut',
	3:'AutoBurnOut',
	4:'StaticBias',
	5:'AutoGateSweep',
	6:'DeviceHistory',
	7:'ChipHistory'
}

default_parameters = {
	'chipID':chipID,
	'deviceID':deviceID,
	'saveFolder':saveFolder,
	'NPLC':1
}

additional_parameters = {
	'GateSweep':{
		'saveFileName': 'GateSweep_' + chipID,
		'runDataPoints':600,
		'complianceCurrent':	100e-6,
		'drainVoltageSetPoint':	0.5,
		'gateVoltageMinimum':	-15.0,
		'gateVoltageMaximum':	15.0
	},
	'BurnOut':{
		'saveFileName': 'BurnOut_' + chipID,
		'runDataPoints':1000,
		'complianceCurrent':	2000e-6,
		'thresholdProportion':	0.8,
		'gateVoltageSetPoint':	15.0,
		'drainVoltageMaxPoint':	10,
		'drainVoltagePlateaus': 10
	},
	'AutoBurnOut':{
		'targetOnOffRatio': 100,
		'limitBurnOutsAllowed': 1,
		'limitOnOffRatioDegradation': 0.7
	},
	'StaticBias':{
		'time': 600,
		'complianceCurrent':	100e-6,
		'gateVoltageSetPoint':	-15.0,
		'drainVoltageSetPoint':	0.5,
	},
	'AutoGateSweep':{
		'numberOfSweeps':2,
		'applyStaticBiasBetweenSweeps':False,
		'saveFiguresBetweenSweeps':True
	},
	'DeviceHistory':{
		'saveFiguresGenerated':False,
		'showOnlySuccessfulBurns': False,
		'firstRunToPlot': 0
	},
	'ChipHistory':{

	}
}

def main(parameters):
	while(True):
		os.system('clear')
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
	elif(parameters['runType'] == 'DeviceHistory'):
		deviceHistoryScript.run(parameters)
	elif(parameters['runType'] == 'ChipHistory'):
		chipHistoryScript.run(parameters)
	else:
		raise NotImplementedError("Invalid action for the B2912A Source Measure Unit")

def print_dict(dict):
	keys = list(dict.keys())
	for i in range(len(keys)):
		print('  ' + str(keys[i]) + ': ' + str(dict[keys[i]]))


if __name__ == '__main__':
    main(default_parameters)