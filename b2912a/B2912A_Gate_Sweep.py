import time
import numpy as np

from utilities import DataLoggerUtility as dlu
from utilities import DataGeneratorUtility as dgu
from utilities import DataPlotterUtility as dpu
from framework import SourceMeasureUnit as smu



# ## ********** Parameters **********

# chipID = 'C127-'
# deviceID = '0-0'

# #saveFolder = '/Users/stevennoyce/Documents/home/Research/illumina/PSoC/Layout 2_14/Version 2/Host/Testing/'
# saveFolder = '/Users/jaydoherty/Documents/myWorkspaces/Python/Research/CNT_IV/b2912a/data/'
# saveFileName = 'GateSweep_' + chipID

# default_parameters = {
# 	'runType':'GateSweep',
# 	'chipID':chipID,
# 	'deviceID':deviceID,
# 	'saveFolder':saveFolder,
# 	'saveFileName':saveFileName,
# 	'NPLC':1,
# 	'runDataPoints':600,
# 	'complianceCurrent':	50e-6,
# 	'drainVoltageSetPoint':	0.5,
# 	'gateVoltageMinimum':	-15.0,
# 	'gateVoltageMaximum':	15.0
# }



## ********** Main **********

def run(parameters, smu_instance, isSavingResults=True, isPlottingResults=True):
	dlu.makeFolder(parameters['deviceDirectory'])
	dlu.initCSV(parameters['deviceDirectory'], parameters['GateSweep']['saveFileName'])
	smu_instance.setComplianceCurrent(parameters['GateSweep']['complianceCurrent'])	

	smu_instance.rampDrainVoltageTo(parameters['GateSweep']['drainVoltageSetPoint'], 20)
	results = runGateSweep( smu_instance, 
							parameters['deviceDirectory'], 
							parameters['GateSweep']['saveFileName'], 
							parameters['GateSweep']['drainVoltageSetPoint'],
							parameters['GateSweep']['gateVoltageMinimum'], 
							parameters['GateSweep']['gateVoltageMaximum'], 
							parameters['GateSweep']['runDataPoints'],
							parameters['NPLC'])
	smu_instance.rampDownVoltages()

	jsonData = {**parameters, **results}
	
	print('On/Off ratio: {:.4f}'.format(results['onOffRatio']))
	print('On current: {:.4e}'.format(results['onCurrent']))
	print('Off current: {:.4e}'.format(results['offCurrent']))

	if(isSavingResults):
		dlu.saveJSON(parameters['deviceDirectory'], parameters['GateSweep']['saveFileName'], jsonData)

	if(isPlottingResults):
		dpu.plotJSON(jsonData, parameters, 'b')
		dpu.show()
		
	return jsonData


def runGateSweep(smu_instance, workingDirectory, saveFileName, drainVoltageSetPoint, gateVoltageMinimum, gateVoltageMaximum, steps, NPLC):
	voltage1s = [[],[]]
	current1s = [[],[]]
	voltage2s = [[],[]]
	current2s = [[],[]]
	timestamps = [[],[]]

	smu_instance.rampGateVoltage(0, gateVoltageMinimum, 20)
	gateVoltages = dgu.sweepValuesWithDuplicates(gateVoltageMinimum, gateVoltageMaximum, steps, 3)
	
	#forward_measurements = smu_instance.takeSweep(drainVoltageSetPoint, drainVoltageSetPoint, gateVoltageMinimum, gateVoltageMaximum, steps/2, NPLC)
	#reverse_measurements = smu_instance.takeSweep(drainVoltageSetPoint, drainVoltageSetPoint, gateVoltageMaximum, gateVoltageMinimum, steps/2, NPLC)
	#timestamp = time.time()

	for i in [0,1]:
		for gateVoltage in gateVoltages[i]:
			smu_instance.setVgs(gateVoltage)
			measurement = smu_instance.takeMeasurement()
			
			voltage1 = measurement['V_ds']
			current1 = measurement['I_d']
			voltage2 = measurement['V_gs']
			current2 = measurement['I_g']
			timestamp = time.time()

			csvData = [timestamp, voltage1, current1, voltage2, current2]
			dlu.saveCSV(workingDirectory, saveFileName, csvData)
			
			voltage1s[i].append(voltage1)
			current1s[i].append(current1)
			voltage2s[i].append(voltage2)
			current2s[i].append(current2)
			timestamps[i].append(timestamp)

	return {
		'voltage1s':voltage1s,
		'current1s':current1s,
		'voltage2s':voltage2s,
		'current2s':current2s,
		'timestamps':timestamps,
		'gateVoltages':gateVoltages,
		'onOffRatio':onOffRatio(current1s),
		'onCurrent':onCurrent(current1s),
		'offCurrent':offCurrent(current1s)
	}

def onOffRatio(drainCurrent):
	return onCurrent(drainCurrent)/offCurrent(drainCurrent)

def onCurrent(drainCurrent):
	absDrainCurrent = abs(np.array(drainCurrent))
	return np.percentile(absDrainCurrent, 99)

def offCurrent(drainCurrent):
	absDrainCurrent = abs(np.array(drainCurrent))
	return (np.percentile(absDrainCurrent, 5))

	

if __name__ == '__main__':
    run(default_parameters)