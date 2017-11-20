import os

import B2912A_Burn_Out_v1 as burnOutScript
import B2912A_Gate_Sweep_v2 as gateSweepScript
import B2912A_Auto_Burn_Out_v1 as autoBurnScript
import Device_History as deviceHistoryScript
import Chip_History as chipHistoryScript

## ********** Parameters **********

chipID = 'C127M'
deviceID = '19-20'

#saveFolder = '/Users/stevennoyce/Documents/home/Research/illumina/PSoC/Layout 2_14/Version 2/Host/Testing/'
saveFolder = '/Users/jaydoherty/Documents/myWorkspaces/Python/Research/b2912a/data/'

runTypes = {
	0:'Quit',
	1:'GateSweep',
	2:'BurnOut',
	3:'AutoBurnOut',
	4:'DeviceHistory',
	5:'ChipHistory'
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
		'limitBurnOutsAllowed': 8,
		'limitOnOffRatioDegradation': 0.7
	},
	'DeviceHistory':{

	},
	'ChipHistory':{

	}
}

def main(parameters):
	while(True):
		os.system('clear')
		print('Actions: ')
		print_dict(runTypes)
		choice = int(input('Choose an action (1,2,...): '))

		if(choice == 0):
			break

		parameters = {'runType': runTypes[choice]}
		parameters = {**parameters, **default_parameters}
		parameters = {**parameters, **additional_parameters[runTypes[choice]]}

		print('Parameters: ')
		print_dict(parameters)
		confirmation = str(input('Are parameters correct? (y/n):'))

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