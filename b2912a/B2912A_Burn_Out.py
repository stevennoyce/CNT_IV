from matplotlib import pyplot as plt
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
# saveFileName = 'BurnOut_' + chipID

# default_parameters = {
# 	'runType':'BurnOut',
# 	'chipID':chipID,
# 	'deviceID':deviceID,
# 	'saveFolder':saveFolder,
# 	'saveFileName':saveFileName,
# 	'NPLC':					1,
# 	'runDataPoints':		200,
# 	'complianceCurrent': 	2000e-6,
# 	'thresholdProportion':	0.8,
# 	'gateVoltageSetPoint':	15.0,
# 	'drainVoltageMaxPoint':	10.0,
# 	'drainVoltagePlateaus':	10
# }



## ********** Main **********

def run(parameters, isSavingResults=True, isPlottingResults=True):
	dlu.makeFolder(parameters['saveFolder'])
	dlu.initCSV(parameters['saveFolder'], parameters['saveFileName'])

	smu_instance = smu.getConnectionFromVisa(parameters['NPLC'], parameters['complianceCurrent'])
	#smu_instance = smu.SimulationSMU()

	smu_instance.rampGateVoltage(0, parameters['gateVoltageSetPoint'], 20)
	results = runBurnOutSweep(	smu_instance, 
								parameters['saveFolder'], 
								parameters['saveFileName'], 
								parameters['thresholdProportion'], 
								0, 
								parameters['drainVoltageMaxPoint'], 
								parameters['drainVoltagePlateaus'], 
								parameters['runDataPoints'])
	smu_instance.rampDownVoltages()

	jsonData = {**parameters, **results}

	if(isSavingResults):
		dlu.saveJSON(parameters['saveFolder'], parameters['saveFileName'], jsonData)

	if(isPlottingResults):
		dpu.plotJSON(jsonData, 'b')
		dpu.show()

	return jsonData

def runBurnOutSweep(smu_instance, saveFolder, saveFileName, thresholdProportion, voltageStart, voltageSetPoint, voltagePlateaus, points):
	current1_threshold = -1
	burned = False
	voltage1s = []
	current1s = []
	voltage2s = []
	current2s = []
	timestamps = []

	drainVoltages = dgu.stepValues(voltageStart, voltageSetPoint, voltagePlateaus, points)

	for drainVoltage in drainVoltages:
		smu_instance.setParameter(":source1:voltage {}".format(drainVoltage))
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

		current1_threshold = np.percentile(np.array(current1s), 90) * thresholdProportion

		if(thresholdCrossed(current1_threshold, current1)):
			burned = True
			break

	smu_instance.rampDrainVoltage(drainVoltage, 0, 20)

	return {
		'voltage1s':voltage1s,
		'current1s':current1s,
		'voltage2s':voltage2s,
		'current2s':current2s,
		'timestamps':timestamps,
		'drainVoltages':drainVoltages,
		'didBurnOut':burned,
		'thresholdCurrent':current1_threshold
	}

def thresholdCrossed(threshold, current):
	return (current < (threshold)) and (threshold > 50e-9)


	

if __name__ == '__main__':
	run(default_parameters)