# === Imports ===
import time
import numpy as np

from control_scripts import Device_History as deviceHistoryScript
from utilities import DataLoggerUtility as dlu
from utilities import DataGeneratorUtility as dgu
from utilities import DataPlotterUtility as dpu
#from framework import SourceMeasureUnit as smu



# === Main ===
def run(parameters, smu_instance, isSavingResults=True, isPlottingResults=True):
	# Create distinct parameters for plotting the results
	deviceHistoryParameters = dict(parameters)
	deviceHistoryParameters['runType'] = 'DeviceHistory'
	deviceHistoryParameters['DeviceHistory']['plotGateSweeps'] = False
	deviceHistoryParameters['DeviceHistory']['plotBurnOuts'] = True
	deviceHistoryParameters['DeviceHistory']['plotStaticBias'] = False
	deviceHistoryParameters['DeviceHistory']['saveFiguresGenerated'] = True
	deviceHistoryParameters['DeviceHistory']['excludeDataBeforeJSONIndex'] = 0
	deviceHistoryParameters['DeviceHistory']['excludeDataAfterJSONIndex'] =  float('inf')
	deviceHistoryParameters['DeviceHistory']['excludeDataBeforeJSONExperimentNumber'] = parameters['startIndexes']['experimentNumber']
	deviceHistoryParameters['DeviceHistory']['excludeDataAfterJSONExperimentNumber'] =  parameters['startIndexes']['experimentNumber']

	print('Attempting to burnout metallic CNTs: V_GS='+str(parameters['BurnOut']['gateVoltageSetPoint'])+'V, max V_DS='+str(parameters['BurnOut']['drainVoltageMaxPoint'])+'V')
	smu_instance.setComplianceCurrent(parameters['BurnOut']['complianceCurrent'])	

	# === START ===
	smu_instance.rampGateVoltageTo(parameters['BurnOut']['gateVoltageSetPoint'])
	results = runBurnOutSweep(	smu_instance, 
								thresholdProportion=parameters['BurnOut']['thresholdProportion'], 
								minimumAppliedDrainVoltage=parameters['BurnOut']['minimumAppliedDrainVoltage'],
								voltageStart=0, 
								voltageSetPoint=parameters['BurnOut']['drainVoltageMaxPoint'], 
								voltagePlateaus=parameters['BurnOut']['drainVoltagePlateaus'], 
								pointsPerRamp=parameters['BurnOut']['pointsPerRamp'],
								pointsPerHold=parameters['BurnOut']['pointsPerHold'])
	smu_instance.rampDownVoltages()

	# Copy parameters and add in the test results
	jsonData = dict(parameters)
	jsonData['Results'] = results

	print('Did it burn?: '+str('Yes' if(results['didBurnOut']) else 'No'))

	# Save results as a JSON object
	if(isSavingResults):
		dlu.saveJSON(dlu.getDeviceDirectory(parameters), parameters['BurnOut']['saveFileName'], jsonData)

	# Show plots to the user
	if(isPlottingResults):
		deviceHistoryScript.run(deviceHistoryParameters, showFigures=True)

	return jsonData

# === Data Collection ===
def runBurnOutSweep(smu_instance, thresholdProportion, minimumAppliedDrainVoltage, voltageStart, voltageSetPoint, voltagePlateaus, pointsPerRamp, pointsPerHold):
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

