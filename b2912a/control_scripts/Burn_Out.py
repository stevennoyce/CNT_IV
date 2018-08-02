# === Imports ===
import time
import numpy as np

from control_scripts import Device_History as deviceHistoryScript
from utilities import DataLoggerUtility as dlu
from utilities import DataGeneratorUtility as dgu



# === Main ===
def run(parameters, smu_instance, isSavingResults=True, isPlottingResults=False):
	# Create distinct parameters for plotting the results
	dh_parameters = {}
	dh_parameters['Identifiers'] = dict(parameters['Identifiers'])
	dh_parameters['dataFolder'] = parameters['dataFolder']
	dh_parameters['plotGateSweeps'] = False
	dh_parameters['plotBurnOuts'] = True
	dh_parameters['plotStaticBias'] = False
	dh_parameters['showFiguresGenerated'] = True
	dh_parameters['saveFiguresGenerated'] = True
	dh_parameters['excludeDataBeforeJSONExperimentNumber'] = parameters['startIndexes']['experimentNumber']
	dh_parameters['excludeDataAfterJSONExperimentNumber'] =  parameters['startIndexes']['experimentNumber']

	# Get shorthand name to easily refer to configuration parameters
	bo_parameters = parameters['runConfigs']['BurnOut']
	
	# Print the starting message
	print('Attempting to burnout metallic CNTs: V_GS='+str(bo_parameters['gateVoltageSetPoint'])+'V, max V_DS='+str(bo_parameters['drainVoltageMaxPoint'])+'V')
	smu_instance.setComplianceCurrent(bo_parameters['complianceCurrent'])	

	# === START ===
	# Apply gate voltage to turn off semiconducting CNTs
	print('Ramping gate voltage.')
	smu_instance.rampGateVoltageTo(bo_parameters['gateVoltageSetPoint'])
	
	print('Begining to ramp drain voltage.')
	results = runBurnOutSweep(	smu_instance, 
								thresholdProportion=bo_parameters['thresholdProportion'], 
								minimumAppliedDrainVoltage=bo_parameters['minimumAppliedDrainVoltage'],
								voltageStart=0, 
								voltageSetPoint=bo_parameters['drainVoltageMaxPoint'], 
								voltagePlateaus=bo_parameters['drainVoltagePlateaus'], 
								pointsPerRamp=bo_parameters['pointsPerRamp'],
								pointsPerHold=bo_parameters['pointsPerHold'])
	smu_instance.rampDownVoltages()
	# === COMPLETE ===

	# Add important metrics from the run to the parameters for easy access later in ParametersHistory
	parameters['Computed'] = results['Computed']
	
	# Print the metrics
	print('Did it burn?: '+str('Yes' if(results['Computed']['didBurnOut']) else 'No'))
	print('max drain current: ' + str(max(results['Raw']['id_data'])))

	# Copy parameters and add in the test results
	jsonData = dict(parameters)
	jsonData['Results'] = results['Raw']

	# Save results as a JSON object
	if(isSavingResults):
		print('Saving JSON.')
		dlu.saveJSON(dlu.getDeviceDirectory(parameters), bo_parameters['saveFileName'], jsonData)

	# Show plots to the user
	if(isPlottingResults):
		deviceHistoryScript.run(dh_parameters)

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
		'Raw':{
			'vds_data':vds_data,
			'id_data':id_data,
			'vgs_data':vgs_data,
			'ig_data':ig_data,
			'timestamps':timestamps,
			'drainVoltages':drainVoltages
		},
		'Computed':{
			'didBurnOut':burned,
			'thresholdCurrent':id_threshold
		}
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

