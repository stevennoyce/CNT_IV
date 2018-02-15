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

def run(parameters, smu_instance, isSavingResults=True, isPlottingResults=True):
	print('Attempting to burnout metallic CNTs: V_GS='+str(parameters['BurnOut']['gateVoltageSetPoint'])+'V, max V_DS='+str(parameters['BurnOut']['drainVoltageMaxPoint'])+'V')
	
	dlu.makeFolder(parameters['deviceDirectory'])
	dlu.initCSV(parameters['deviceDirectory'], parameters['BurnOut']['saveFileName'])
	smu_instance.setComplianceCurrent(parameters['BurnOut']['complianceCurrent'])	

	smu_instance.rampGateVoltageTo(parameters['BurnOut']['gateVoltageSetPoint'], 20)
	results = runBurnOutSweep(	smu_instance, 
								parameters['deviceDirectory'], 
								parameters['BurnOut']['saveFileName'], 
								parameters['BurnOut']['thresholdProportion'], 
								parameters['BurnOut']['minimumAppliedDrainVoltage'],
								0, 
								parameters['BurnOut']['drainVoltageMaxPoint'], 
								parameters['BurnOut']['drainVoltagePlateaus'], 
								parameters['BurnOut']['runDataPoints'])
	smu_instance.rampDownVoltages()

	jsonData = {**parameters, **results}

	if(isSavingResults):
		dlu.saveJSON(parameters['deviceDirectory'], parameters['BurnOut']['saveFileName'], jsonData)

	if(isPlottingResults):
		dpu.plotJSON(jsonData, parameters, 'b')
		dpu.show()

	return jsonData

def runBurnOutSweep(smu_instance, workingDirectory, saveFileName, thresholdProportion, minimumAppliedDrainVoltage, voltageStart, voltageSetPoint, voltagePlateaus, points):
	current1_threshold = -1
	burned = False
	voltage1s = []
	current1s = []
	voltage2s = []
	current2s = []
	timestamps = []

	drainVoltages = dgu.stepValues(voltageStart, voltageSetPoint, voltagePlateaus, points)

	for i, drainVoltage in enumerate(drainVoltages):
		smu_instance.setVds(drainVoltage)
		measurement = smu_instance.takeMeasurement()

		voltage1 = measurement['V_ds']
		current1 = measurement['I_d']
		voltage2 = measurement['V_gs']
		current2 = measurement['I_g']
		timestamp = time.time()

		csvData = [timestamp, voltage1, current1, voltage2, current2]
		dlu.saveCSV(workingDirectory, saveFileName, csvData)

		voltage1s.append(voltage1)
		current1s.append(current1)
		voltage2s.append(voltage2)
		current2s.append(current2)
		timestamps.append(timestamp)
		
		current1_threshold = np.percentile(np.array(current1s), 90) * thresholdProportion
		current1_recent_measurements = [current1]

		if(drainVoltages[i] == drainVoltages[i-1]):
			current1_recent_measurements = current1s[-3:]

		if(thresholdCrossed(current1_threshold, current1_recent_measurements, drainVoltages[i], minimumAppliedDrainVoltage)):
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

def thresholdCrossed(threshold, recent_measurements, drainVoltage, minimumAppliedDrainVoltage):
	if(threshold < 50e-9):
		return False

	if(drainVoltage < minimumAppliedDrainVoltage):
		return False

	for current in recent_measurements: 
		if(current > threshold):
			return False

	return True


	

if __name__ == '__main__':
	run(default_parameters)