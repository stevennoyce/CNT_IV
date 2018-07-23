# === Imports ===
import time
import numpy as np

from control_scripts import Device_History as deviceHistoryScript
from utilities import DataLoggerUtility as dlu
#from framework import SourceMeasureUnit as smu



# === Main ===
def run(parameters, smu_instance, arduino_instance, isSavingResults=True, isPlottingResults=False):
	# Create distinct parameters for plotting the results
	dh_parameters = {}
	dh_parameters['Identifiers'] = dict(parameters['Identifiers'])
	dh_parameters['dataFolder'] = parameters['dataFolder']
	dh_parameters['plotGateSweeps'] = False
	dh_parameters['plotBurnOuts'] = False
	dh_parameters['plotStaticBias'] = True
	dh_parameters['showFiguresGenerated'] = True
	dh_parameters['saveFiguresGenerated'] = True
	dh_parameters['excludeDataBeforeJSONExperimentNumber'] = parameters['startIndexes']['experimentNumber']
	dh_parameters['excludeDataAfterJSONExperimentNumber'] =  parameters['startIndexes']['experimentNumber']

	sb_parameters = parameters['runConfigs']['StaticBias']

	print('Applying static bias of V_GS='+str(sb_parameters['gateVoltageSetPoint'])+'V, V_DS='+str(sb_parameters['drainVoltageSetPoint'])+'V for '+str(sb_parameters['totalBiasTime'])+' seconds...')
	smu_instance.setComplianceCurrent(sb_parameters['complianceCurrent'])	

	# Ensure all sensor data is reset to empty lists so that there is one-to-one mapping between device and sensor measurements
	sensor_data = arduino_instance.takeMeasurement()
	for (measurement, value) in sensor_data.items():
		parameters['SensorData'][measurement] = []

	# === START ===
	# Delay before applying voltage (can be used in AutoStaticBias to hold the device grounded between runs)
	if(sb_parameters['delayBeforeApplyingVoltage'] > 0):
		time.sleep(sb_parameters['delayBeforeApplyingVoltage'])

	smu_instance.rampDrainVoltageTo(sb_parameters['drainVoltageSetPoint'])
	smu_instance.rampGateVoltageTo(sb_parameters['gateVoltageSetPoint'])

	# Delay before measurements begin (only useful for allowing current to settle a little, not usually necessary)
	if(sb_parameters['delayBeforeMeasurementsBegin'] > 0):
		time.sleep(sb_parameters['delayBeforeMeasurementsBegin'])

	results = runStaticBias(smu_instance, 
							arduino_instance,
							drainVoltageSetPoint=sb_parameters['drainVoltageSetPoint'],
							gateVoltageSetPoint=sb_parameters['gateVoltageSetPoint'],
							totalBiasTime=sb_parameters['totalBiasTime'], 
							measurementTime=sb_parameters['measurementTime'])
	smu_instance.rampGateVoltageTo(sb_parameters['gateVoltageWhenDone'])
	smu_instance.rampDrainVoltageTo(sb_parameters['drainVoltageWhenDone'])

	# Copy parameters and add in the test results
	parameters['Computed'] = results['Computed']

	jsonData = dict(parameters)
	jsonData['Results'] = results['Raw']
	
	# Save results as a JSON object
	if(isSavingResults):
		print('Saving JSON.')
		dlu.saveJSON(dlu.getDeviceDirectory(parameters), sb_parameters['saveFileName'], jsonData)
	
	# Show plots to the user
	if(isPlottingResults):
		deviceHistoryScript.run(dh_parameters)
	
	return jsonData

# === Data Collection ===
def runStaticBias(smu_instance, arduino_instance, drainVoltageSetPoint, gateVoltageSetPoint, totalBiasTime, measurementTime):
	vds_data = []
	id_data = []
	vgs_data = []
	ig_data = []
	timestamps = []

	steps = int(totalBiasTime/measurementTime)
	pointsToAverageOver = (measurementTime)*(smu_instance.measurementsPerSecond)/(smu_instance.nplc)/1.5
	
	startTime = time.time()
	
	for i in range(steps):
		# Take a 'sweep' at static voltage to get many measurements. Sweep takes 'measurementTime' number of seconds to complete.
		# measurements = smu_instance.takeSweep(drainVoltageSetPoint, drainVoltageSetPoint, gateVoltageSetPoint, gateVoltageSetPoint, pointsToAverageOver)
		
		measurements = smu_instance.takeSweep(drainVoltageSetPoint, drainVoltageSetPoint, gateVoltageSetPoint, gateVoltageSetPoint, int(1/4*pointsToAverageOver))
		
		while time.time() - startTime < measurementTime*(i+3/4):
			measurement = smu_instance.takeSweep(drainVoltageSetPoint, drainVoltageSetPoint, gateVoltageSetPoint, gateVoltageSetPoint, int(1/4*pointsToAverageOver))
			for key, value in measurement.items():
				if isinstance(value, list):
					measurements[key].extend(value)
		
		timestamp = time.time()
		
		
		# Save the median of the sweep as this measurement
		vds_data.append(np.median(measurements['Vds_data']))
		id_data.append(np.median(measurements['Id_data']))
		vgs_data.append(np.median(measurements['Vgs_data']))
		ig_data.append(np.median(measurements['Ig_data']))
		timestamps.append(timestamp)

		# Take a measurement with the Arduino
		sensor_data = arduino_instance.takeMeasurement()
		for (measurement, value) in sensor_data.items():
			parameters['SensorData'][measurement].append(value)

		print('\r[' + int(i*70.0/steps)*'=' + (70-int(i*70.0/steps)-1)*' ' + ']', end='')
	print('')

	return {
		'Raw':{
			'vds_data':vds_data,
			'id_data':id_data,
			'vgs_data':vgs_data,
			'ig_data':ig_data,
			'timestamps':timestamps
		},
		'Computed':{
			'id_std':drainCurrentSTD(id_data)
		}
	}

def drainCurrentSTD(drainCurrent):
	return np.std(drainCurrent)

