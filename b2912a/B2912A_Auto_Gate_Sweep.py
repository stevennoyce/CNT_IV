import time

import B2912A_Gate_Sweep as gateSweepScript
import B2912A_Static_Bias as staticBiasScript
import Device_History as deviceHistoryScript
from utilities import DataLoggerUtility as dlu



# ## ********** Parameters **********

# chipID = 'C127-'

# default_parameters = {
# 	'runType':		'AutoGateSweep',
# 	'chipID':		chipID,
# 	'deviceID':		'0-0',
# 	'saveFolder':	'/Users/jaydoherty/Documents/myWorkspaces/Python/Research/CNT_IV/b2912a/data/',
# 	'NPLC':1,
# 	'numberOfSweeps':3,
# 	'applyStaticBiasBetweenSweeps':True,
# 	'GateSweep':{
# 		'saveFileName': 'GateSweep',
# 		'runDataPoints':600,
# 		'complianceCurrent':	100e-6,
# 		'drainVoltageSetPoint':	0.5,
# 		'gateVoltageMinimum':	-15.0,
# 		'gateVoltageMaximum':	15.0
# 	},
# 	'StaticBias':{
# 		'time': 30,
# 		'complianceCurrent':	100e-6,
# 		'gateVoltageSetPoint':	-15.0,
# 		'drainVoltageSetPoint':	0.5,
# 	}
# }


def run(parameters):
	gateSweepParameters = dict(parameters)
	gateSweepParameters['runType'] = 'GateSweep'
	gateSweepParameters = {**gateSweepParameters, **parameters['GateSweep']}

	staticBiasParameters = dict(parameters)
	staticBiasParameters['runType'] = 'StaticBias'
	staticBiasParameters = {**staticBiasParameters, **parameters['StaticBias']}
	
	deviceHistoryParameters = {
		'runType':'DeviceHistory', 
		'chipID':parameters['chipID'], 
		'deviceID':parameters['deviceID'],
		'saveFolder':parameters['dataFolder'],
		'postFigures':parameters['postFigures'],
		'NPLC':parameters['NPLC'],
		'plotGateSweeps': True,
		'plotBurnOuts': False,
		'plotStaticBias': parameters['applyStaticBiasBetweenSweeps'],
		'saveFiguresGenerated':True,
		'excludeDataBeforeJSONIndex': 0,
		'excludeDataAfterJSONIndex':  float('inf'),
		'excludeDataBeforeJSONExperimentNumber': parameters['startIndexes']['experimentNumber'],
		'excludeDataAfterJSONExperimentNumber':  parameters['startIndexes']['experimentNumber'],
		'showOnlySuccessfulBurns': False
	}

	runAutoGateSweep(parameters, gateSweepParameters, staticBiasParameters, deviceHistoryParameters)

	deviceHistoryScript.run(deviceHistoryParameters, showFigures=True)
	

def runAutoGateSweep(parameters, gateSweepParameters, staticBiasParameters, deviceHistoryParameters):
	numberOfSweeps = parameters['numberOfSweeps']
	sweepCount = 0

	while(sweepCount < numberOfSweeps):
		gateSweepScript.run(gateSweepParameters, isSavingResults=True, isPlottingResults=False)
		if(parameters['applyStaticBiasBetweenSweeps']):
			staticBiasScript.run(staticBiasParameters, isSavingResults=True, isPlottingResults=False)
		deviceHistoryScript.run(deviceHistoryParameters, showFigures=False)
		sweepCount += 1
		print('Completed sweep #'+str(sweepCount)+' of '+str(numberOfSweeps))
		






if __name__ == '__main__':
	run(default_parameters)