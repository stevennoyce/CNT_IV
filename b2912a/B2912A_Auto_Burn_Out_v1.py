import B2912A_Burn_Out_v1 as burnOutScript
import B2912A_Gate_Sweep_v2 as gateSweepScript
import Device_History as deviceHistoryScript



# ## ********** Parameters **********

# chipID = 'C127-'
# deviceID = '0-0'

# #saveFolder = '/Users/stevennoyce/Documents/home/Research/illumina/PSoC/Layout 2_14/Version 2/Host/Testing/'
# saveFolder = '/Users/jaydoherty/Documents/myWorkspaces/Python/Research/b2912a/data/'

# default_parameters = {
# 	'runType':'AutoBurnOut',
# 	'chipID':chipID,
# 	'deviceID':deviceID,
# 	'saveFolder':saveFolder,
# 	'NPLC':1,
# 	'targetOnOffRatio': 100,
# 	'limitBurnOutsAllowed': 8,
# 	'limitOnOffRatioDegradation': 0.9,
# 	'GateSweep':{
# 		'saveFileName': 'GateSweep_' + chipID,
# 		'runDataPoints':600,
# 		'complianceCurrent':	80e-6,
# 		'drainVoltageSetPoint':	0.5,
# 		'gateVoltageMinimum':	-15.0,
# 		'gateVoltageMaximum':	15.0
# 	},
# 	'BurnOut':{
# 		'saveFileName': 'BurnOut_' + chipID,
# 		'runDataPoints':1000,
# 		'complianceCurrent':	2000e-6,
# 		'thresholdProportion':	0.75,
# 		'gateVoltageSetPoint':	15.0,
# 		'drainVoltageMaxPoint':	10,
# 		'drainVoltagePlateaus': 10
# 	}
# }



def run(parameters):
	gateSweepParameters = {	
		'runType':'GateSweep', 
		'chipID':parameters['chipID'], 
		'deviceID':parameters['deviceID'],
		'saveFolder':parameters['saveFolder'],
		'NPLC':parameters['NPLC']
	}
	gateSweepParameters = {**gateSweepParameters, **parameters['GateSweep']}

	burnOutParameters = {
		'runType':'BurnOut',
		'chipID':parameters['chipID'], 
		'deviceID':parameters['deviceID'],
		'saveFolder':parameters['saveFolder'],
		'NPLC':parameters['NPLC']
	}
	burnOutParameters = {**burnOutParameters, **parameters['BurnOut']}

	targetOnOffRatio = parameters['targetOnOffRatio']
	allowedDegradationFactor = parameters['limitOnOffRatioDegradation']
	burnOutLimit = parameters['limitBurnOutsAllowed']
	burnOutCount = 0

	sweepResults = gateSweepScript.run(gateSweepParameters, True, False)
	previousOnOffRatio = sweepResults['onOffRatio']

	while((previousOnOffRatio < targetOnOffRatio) and (burnOutCount < burnOutLimit)):
		burnOutScript.run(burnOutParameters, True, False)
		sweepResults = gateSweepScript.run(gateSweepParameters, True, False)
		currentOnOffRatio = sweepResults['onOffRatio']

		if(currentOnOffRatio < allowedDegradationFactor*previousOnOffRatio):
			break

		burnOutCount += 1
		previousOnOffRatio = currentOnOffRatio

	deviceHistoryScript.run(parameters)



if __name__ == '__main__':
	run(default_parameters)