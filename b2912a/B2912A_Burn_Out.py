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
	
	smu_instance.setComplianceCurrent(parameters['BurnOut']['complianceCurrent'])	

	# RUN TEST
	smu_instance.rampGateVoltageTo(parameters['BurnOut']['gateVoltageSetPoint'], 20)
	results = runBurnOutSweep(	smu_instance, 
								parameters['deviceDirectory'], 
								parameters['BurnOut']['saveFileName'], 
								parameters['BurnOut']['thresholdProportion'], 
								parameters['BurnOut']['minimumAppliedDrainVoltage'],
								0, 
								parameters['BurnOut']['drainVoltageMaxPoint'], 
								parameters['BurnOut']['drainVoltagePlateaus'], 
								parameters['BurnOut']['pointsPerRamp'],
								parameters['BurnOut']['pointsPerHold'])
	smu_instance.rampDownVoltages()

	# Copy parameters and add in the test results
	jsonData = dict(parameters)
	jsonData['Results'] = results

	# Save results as a JSON object
	if(isSavingResults):
		dlu.saveJSON(parameters['deviceDirectory'], parameters['BurnOut']['saveFileName'], jsonData)

	# Show plots to the user
	if(isPlottingResults):
		dpu.plotJSON(jsonData, parameters, 'b')
		dpu.show()

	return jsonData

def runBurnOutSweep(smu_instance, workingDirectory, saveFileName, thresholdProportion, minimumAppliedDrainVoltage, voltageStart, voltageSetPoint, voltagePlateaus, pointsPerRamp, pointsPerHold):
	burned = False
	vds_data = []
	id_data = []
	vgs_data = []
	ig_data = []
	timestamps = []

	drainVoltages = dgu.stepValues(voltageStart, voltageSetPoint, voltagePlateaus, pointsPerRamp, pointsPerHold)

	for i, drainVoltage in enumerate(drainVoltages):
		# Apply V_DS
		smu_instance.setVds(drainVoltage)

		# Take measurement and save it
		measurement = smu_instance.takeMeasurement()
		timestamp = time.time()

		vds_data.append(measurement['V_ds'])
		id_data.append(measurement['I_d'])
		vgs_data.append(measurement['V_gs'])
		ig_data.append(measurement['I_g'])
		timestamps.append(timestamp)
		
		# Re-compute threshold as a function of all measurements so far
		id_threshold = np.percentile(np.array(id_data), 90) * thresholdProportion
		
		# If we are in a plateau, consider last 3 points, if we are in a rise just look at a single point
		if(drainVoltages[i] == drainVoltages[i-1]):
			id_recent_measurements = id_data[-3:]
		else:
			id_recent_measurements = [measurement['I_d']]

		# Check if threshold has been crossed
		if(thresholdCrossed(id_threshold, id_recent_measurements, drainVoltages[i], minimumAppliedDrainVoltage)):
			burned = True
			break
			
	# Rapidly ramp down V_DS
	smu_instance.rampDrainVoltage(drainVoltage, 0, 20)

	return {
		'vds_data':vds_data,
		'id_data':id_data,
		'vgs_data':vgs_data,
		'ig_data':ig_data,
		'timestamps':timestamps,
		'drainVoltages':drainVoltages,
		'didBurnOut':burned,
		'thresholdCurrent':id_threshold
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