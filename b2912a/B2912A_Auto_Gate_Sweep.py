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
# 		'saveFileName': 'GateSweep_' + chipID,
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
	gateSweepParameters = {	
		'runType':'GateSweep', 
		'chipID':parameters['chipID'], 
		'deviceID':parameters['deviceID'],
		'saveFolder':parameters['saveFolder'],
		'NPLC':parameters['NPLC']
	}
	gateSweepParameters = {**gateSweepParameters, **parameters['GateSweep']}

	staticBiasParameters = {
		'runType':'StaticBias',
		'chipID':parameters['chipID'], 
		'deviceID':parameters['deviceID'],
		'NPLC':parameters['NPLC']
	}
	staticBiasParameters = {**staticBiasParameters, **parameters['StaticBias']}

	numberOfOldDeviceRuns = len(dlu.loadFullDeviceHistory(parameters['saveFolder'], gateSweepParameters['saveFileName']+'.json', parameters['deviceID']))

	deviceHistoryParameters = {
		'runType':'DeviceHistory', 
		'chipID':parameters['chipID'], 
		'deviceID':parameters['deviceID'],
		'saveFolder':parameters['saveFolder'],
		'NPLC':parameters['NPLC'],
		'saveFiguresGenerated':True,
		'showOnlySuccessfulBurns': False,
		'firstRunToPlot': numberOfOldDeviceRuns
	}

	runAutoGateSweep(parameters, gateSweepParameters, staticBiasParameters, deviceHistoryParameters)

	deviceHistoryScript.run(deviceHistoryParameters)

	

def runAutoGateSweep(parameters, gateSweepParameters, staticBiasParameters, deviceHistoryParameters):
	numberOfSweeps = parameters['numberOfSweeps']
	sweepCount = 0

	while(sweepCount < numberOfSweeps):
		if(parameters['applyStaticBiasBetweenSweeps']):
			print('Applying static bias of V_GS='+str(staticBiasParameters['gateVoltageSetPoint'])+'V, V_DS='+str(staticBiasParameters['drainVoltageSetPoint'])+'V for '+str(staticBiasParameters['time'])+' seconds...')
			staticBiasScript.run(staticBiasParameters)
		gateSweepScript.run(gateSweepParameters, True, False)
		deviceHistoryScript.run(deviceHistoryParameters, False)
		sweepCount += 1
		print('Completed sweep #'+str(sweepCount))
		






if __name__ == '__main__':
	run(default_parameters)