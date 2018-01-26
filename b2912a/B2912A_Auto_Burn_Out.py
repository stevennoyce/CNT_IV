import B2912A_Burn_Out as burnOutScript
import B2912A_Gate_Sweep as gateSweepScript
import Device_History as deviceHistoryScript
from utilities import DataLoggerUtility as dlu




# ## ********** Parameters **********

# chipID = 'C127-'
# deviceID = '0-0'

# #saveFolder = '/Users/stevennoyce/Documents/home/Research/illumina/PSoC/Layout 2_14/Version 2/Host/Testing/'
# saveFolder = '/Users/jaydoherty/Documents/myWorkspaces/Python/Research/CNT_IV/b2912a/data/'

# default_parameters = {
# 	'runType':'AutoBurnOut',
# 	'chipID':chipID,
# 	'deviceID':deviceID,
# 	'saveFolder':saveFolder,
# 	'NPLC':1,
# 	'targetOnOffRatio': 100,
# 	'limitBurnOutsAllowed': 8,
# 	'limitOnOffRatioDegradation': 0.7,
# 	'GateSweep':{
# 		'saveFileName': 'GateSweep',
# 		'runDataPoints':600,
# 		'complianceCurrent':	100e-6,
# 		'drainVoltageSetPoint':	0.5,
# 		'gateVoltageMinimum':	-15.0,
# 		'gateVoltageMaximum':	15.0
# 	},
# 	'BurnOut':{
# 		'saveFileName': 'BurnOut',
# 		'runDataPoints':1000,
# 		'complianceCurrent':	2000e-6,
# 		'thresholdProportion':	0.75,
# 		'gateVoltageSetPoint':	15.0,
# 		'drainVoltageMaxPoint':	10,
# 		'drainVoltagePlateaus': 10
# 	}
# }



def run(parameters):
	gateSweepParameters = dict(parameters)
	gateSweepParameters['runType'] = 'GateSweep'
	gateSweepParameters = {**gateSweepParameters, **parameters['GateSweep']}

	burnOutParameters = dict(parameters)
	burnOutParameters['runType'] = 'BurnOut'
	burnOutParameters = {**burnOutParameters, **parameters['BurnOut']}

	workingDirectory = parameters['saveFolder'] + parameters['chipID'] + '/' + parameters['deviceID'] + '/'
	currentExperimentNumber = dlu.loadJSONIndex(workingDirectory)['experimentNumber']

	deviceHistoryParameters = {
		'runType':'DeviceHistory', 
		'chipID':parameters['chipID'], 
		'deviceID':parameters['deviceID'],
		'saveFolder':parameters['saveFolder'],
		'figuresSaved':parameters['figuresSaved'],
		'postFigures':parameters['postFigures'],
		'NPLC':parameters['NPLC'],
		'plotGateSweeps': True,
		'plotBurnOuts': True,
		'plotStaticBias': False,
		'saveFiguresGenerated':True,
		'excludeDataBeforeJSONIndex': 0,
		'excludeDataAfterJSONIndex':  float('inf'),
		'excludeDataBeforeJSONExperimentNumber': currentExperimentNumber,
		'excludeDataAfterJSONExperimentNumber':  currentExperimentNumber,
		'showOnlySuccessfulBurns': False
	}

	runAutoBurnOut(parameters, gateSweepParameters, burnOutParameters, deviceHistoryParameters)

	deviceHistoryScript.run(deviceHistoryParameters)

def runAutoBurnOut(parameters, gateSweepParameters, burnOutParameters, deviceHistoryParameters):
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
		previousOnOffRatio = currentOnOffRatio

		deviceHistoryScript.run(deviceHistoryParameters, False)
		burnOutCount += 1
		print('Completed sweep #'+str(burnOutCount))
		


if __name__ == '__main__':
	run(default_parameters)