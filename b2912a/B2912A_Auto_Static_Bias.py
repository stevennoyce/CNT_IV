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


def run(parameters, smu_instance):
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
		'plotGateSweeps': parameters['applyGateSweepBetweenBiases'],
		'plotBurnOuts': False,
		'plotStaticBias': True,
		'saveFiguresGenerated':True,
		'excludeDataBeforeJSONIndex': 0,
		'excludeDataAfterJSONIndex':  float('inf'),
		'excludeDataBeforeJSONExperimentNumber': parameters['startIndexes']['experimentNumber'],
		'excludeDataAfterJSONExperimentNumber':  parameters['startIndexes']['experimentNumber'],
		'showOnlySuccessfulBurns': False
	}

	runAutoStaticBias(parameters, smu_instance, gateSweepParameters, staticBiasParameters, deviceHistoryParameters)

	deviceHistoryScript.run(deviceHistoryParameters, showFigures=True)
	

def runAutoStaticBias(parameters, smu_instance, gateSweepParameters, staticBiasParameters, deviceHistoryParameters):
	numberOfStaticBiases = parameters['numberOfStaticBiases']
	incrementCount = 0
	biasCount = 0

	while(biasCount < numberOfStaticBiases):
		staticBiasScript.run(staticBiasParameters, smu_instance, isSavingResults=True, isPlottingResults=False)
		if(parameters['applyGateSweepBetweenBiases']):
			gateSweepScript.run(gateSweepParameters, smu_instance, isSavingResults=True, isPlottingResults=False)
		deviceHistoryScript.run(deviceHistoryParameters, showFigures=False)
		if(parameters['delayBetweenBiases'] > 0):
			time.sleep(parameters['delayBetweenBiases'])
		biasCount += 1
		incrementCount += 1
		print('Completed static bias #'+str(biasCount)+' of '+str(numberOfStaticBiases))
		if(incrementCount >= parameters['numberOfBiasesBetweenIncrements']):
			staticBiasParameters['gateVoltageSetPoint'] += parameters['incrementStaticGateVoltage']
			staticBiasParameters['drainVoltageSetPoint'] += parameters['incrementStaticDrainVoltage']
			incrementCount = 0
		






if __name__ == '__main__':
	run(default_parameters)