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

	staticBiasParameters = dict(parameters)
	staticBiasParameters['runType'] = 'StaticBias'
	
	deviceHistoryParameters = dict(parameters)
	deviceHistoryParameters['runType'] = 'DeviceHistory'
	deviceHistoryParameters['DeviceHistory']['plotGateSweeps'] = parameters['AutoStaticBias']['applyGateSweepBetweenBiases']
	deviceHistoryParameters['DeviceHistory']['plotBurnOuts'] = False
	deviceHistoryParameters['DeviceHistory']['plotStaticBias'] = True
	deviceHistoryParameters['DeviceHistory']['saveFiguresGenerated'] = True
	deviceHistoryParameters['DeviceHistory']['excludeDataBeforeJSONIndex'] = 0
	deviceHistoryParameters['DeviceHistory']['excludeDataAfterJSONIndex'] =  float('inf')
	deviceHistoryParameters['DeviceHistory']['excludeDataBeforeJSONExperimentNumber'] = parameters['startIndexes']['experimentNumber']
	deviceHistoryParameters['DeviceHistory']['excludeDataAfterJSONExperimentNumber'] =  parameters['startIndexes']['experimentNumber']
	deviceHistoryParameters['DeviceHistory']['showOnlySuccessfulBurns'] = False

	runAutoStaticBias(parameters, smu_instance, gateSweepParameters, staticBiasParameters, deviceHistoryParameters)

	deviceHistoryScript.run(deviceHistoryParameters, showFigures=True)
	

def runAutoStaticBias(parameters, smu_instance, gateSweepParameters, staticBiasParameters, deviceHistoryParameters):
	numberOfStaticBiases = parameters['AutoStaticBias']['numberOfStaticBiases']
	incrementCount = 0
	biasCount = 0

	while(biasCount < numberOfStaticBiases):
		staticBiasScript.run(staticBiasParameters, smu_instance, isSavingResults=True, isPlottingResults=False)
		if(parameters['AutoStaticBias']['applyGateSweepBetweenBiases']):
			gateSweepScript.run(gateSweepParameters, smu_instance, isSavingResults=True, isPlottingResults=False)
		deviceHistoryScript.run(deviceHistoryParameters, showFigures=False)
		if(parameters['AutoStaticBias']['delayBetweenBiases'] > 0):
			time.sleep(parameters['AutoStaticBias']['delayBetweenBiases'])
		biasCount += 1
		incrementCount += 1
		print('Completed static bias #'+str(biasCount)+' of '+str(numberOfStaticBiases))
		if(incrementCount >= parameters['AutoStaticBias']['numberOfBiasesBetweenIncrements']):
			staticBiasParameters['StaticBias']['gateVoltageSetPoint'] += parameters['AutoStaticBias']['incrementStaticGateVoltage']
			staticBiasParameters['StaticBias']['drainVoltageSetPoint'] += parameters['AutoStaticBias']['incrementStaticDrainVoltage']
			parameters['AutoStaticBias']['delayBetweenBiases'] += parameters['AutoStaticBias']['incrementDelayBetweenBiases']
			if(parameters['incrementallyToggleGrounding']):
				staticBiasParameters['StaticBias']['groundGateWhenDone'] = not staticBiasParameters['StaticBias']['groundGateWhenDone']
				staticBiasParameters['StaticBias']['groundDrainWhenDone'] = (not staticBiasParameters['StaticBias']['groundDrainWhenDone']) and (not staticBiasParameters['StaticBias']['groundGateWhenDone'])
			incrementCount = 0
		






if __name__ == '__main__':
	run(default_parameters)