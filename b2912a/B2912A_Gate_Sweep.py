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

def run(parameters, isSavingResults=True, isPlottingResults=True):
	dlu.makeFolder(parameters['saveFolder'])
	dlu.initCSV(parameters['saveFolder'], parameters['saveFileName'])

	smu_instance = smu.getConnectionFromVisa(parameters['NPLC'], parameters['complianceCurrent'])
	#smu_instance = smu.SimulationSMU()

	smu_instance.rampDrainVoltage(0, parameters['drainVoltageSetPoint'], 20)
	results = runGateSweep( smu_instance, 
							parameters['saveFolder'], 
							parameters['saveFileName'], 
							parameters['gateVoltageMinimum'], 
							parameters['gateVoltageMaximum'], 
							parameters['runDataPoints'])
	smu_instance.rampDownVoltages()

	jsonData = {**parameters, **results}
	
	if(isSavingResults):
		dlu.saveJSON(parameters['saveFolder'], parameters['saveFileName'], jsonData)

	if(isPlottingResults):
		dpu.plotJSON(jsonData, 'b')
		dpu.show()

	return jsonData


def runGateSweep(smu_instance, saveFolder, saveFileName, startVoltage, endVoltage, steps):
	voltage1s = []
	current1s = []
	voltage2s = []
	current2s = []
	timestamps = []

	smu_instance.rampGateVoltage(0, startVoltage, 20)
	gateVoltages = dgu.sweepValuesWithDuplicates(startVoltage, endVoltage, steps, 3)
	
	for gateVoltage in gateVoltages:
		smu_instance.setParameter(":source2:voltage {}".format(gateVoltage))
		measurement = smu_instance.takeMeasurement()
		
		voltage1 = measurement[0]
		current1 = measurement[1]
		voltage2 = measurement[6]
		current2 = measurement[7]
		timestamp = time.time()

		csvData = [timestamp, voltage1, current1, voltage2, current2]
		dlu.saveCSV(saveFolder, saveFileName, csvData)
		
		voltage1s.append(voltage1)
		current1s.append(current1)
		voltage2s.append(voltage2)
		current2s.append(current2)
		timestamps.append(timestamp)

	return {
		'voltage1s':voltage1s,
		'current1s':current1s,
		'voltage2s':voltage2s,
		'current2s':current2s,
		'timestamps':timestamps,
		'gateVoltages':gateVoltages,
		'onOffRatio':onOffRatio(current1s),
		'onCurrent':onCurrent(current1s)
	}

def onOffRatio(drainCurrent):
	absDrainCurrent = abs(np.array(drainCurrent))
	return (np.percentile(absDrainCurrent, 99))/(np.percentile(absDrainCurrent, 5))

def onCurrent(drainCurrent):
	absDrainCurrent = abs(np.array(drainCurrent))
	return np.percentile(absDrainCurrent, 99)

	

if __name__ == '__main__':
    run(default_parameters)