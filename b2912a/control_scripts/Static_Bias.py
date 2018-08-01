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

	if(sb_parameters['floatChannelsWhenDone']):
		print('Turning channels off.')
		smu_instance.turnChannelsOff()

	if(sb_parameters['delayWhenDone'] > 0):
		print('Waiting for: ' + str(sb_parameters['delayWhenDone']) + ' seconds...')
		time.sleep(sb_parameters['delayWhenDone'])
		
	if(sb_parameters['floatChannelsWhenDone']):
		smu_instance.turnChannelsOn()
		print('Channels are back on.')

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

	smu_measurementsPerSecond = smu_instance.measurementsPerSecond
	smu_secondsPerMeasurement = 1/smu_measurementsPerSecond

	steps = int(totalBiasTime/measurementTime) if(measurementTime > 0) else None
	startTime = time.time()

	continueCriterion = lambda i: i < steps
	if(measurementTime < smu_secondsPerMeasurement):
		continueCriterion = lambda i: time.time() - startTime < totalBiasTime
	
	i = 0
	while(continueCriterion(i)):
		i += 1
		
		measurements = {'Vds_data':[], 'Id_data':[], 'Vgs_data':[], 'Ig_data':[]}
		measurement = smu_instance.takeMeasurement()
		measurements['Vds_data'].append(measurement['V_ds'])
		measurements['Id_data'].append(measurement['I_d'])
		measurements['Vgs_data'].append(measurement['V_gs'])
		measurements['Ig_data'].append(measurement['I_g'])

		while time.time() - startTime < measurementTime*i - smu_secondsPerMeasurement/2:
			measurement = smu_instance.takeMeasurement()
			measurements['Vds_data'].append(measurement['V_ds'])
			measurements['Id_data'].append(measurement['I_d'])
			measurements['Vgs_data'].append(measurement['V_gs'])
			measurements['Ig_data'].append(measurement['I_g'])
		
		# Save the median of the measurements
		timestamp = time.time()
		vds_data.append(np.median(measurements['Vds_data']))
		id_data.append(np.median(measurements['Id_data']))
		vgs_data.append(np.median(measurements['Vgs_data']))
		ig_data.append(np.median(measurements['Ig_data']))
		timestamps.append(timestamp)

		# Take a measurement with the Arduino
		sensor_data = arduino_instance.takeMeasurement()
		for (measurement, value) in sensor_data.items():
			parameters['SensorData'][measurement].append(value)

		elapsedTime = time.time() - startTime
		print('\r[' + int(elapsedTime*70.0/totalBiasTime)*'=' + (70-int(elapsedTime*70.0/totalBiasTime)-1)*' ' + ']', end='')
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

