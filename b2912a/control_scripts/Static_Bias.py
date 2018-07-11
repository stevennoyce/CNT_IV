import time
import numpy as np

from utilities import DataLoggerUtility as dlu
from utilities import DataPlotterUtility as dpu
#from framework import SourceMeasureUnit as smu



# === Main ===
def run(parameters, smu_instance, arduino_instance, isSavingResults=True, isPlottingResults=True):
	print('Applying static bias of V_GS='+str(parameters['StaticBias']['gateVoltageSetPoint'])+'V, V_DS='+str(parameters['StaticBias']['drainVoltageSetPoint'])+'V for '+str(parameters['StaticBias']['totalBiasTime'])+' seconds...')
	smu_instance.setComplianceCurrent(parameters['StaticBias']['complianceCurrent'])	

	# Ensure all sensor data is reset to empty lists so that there is one-to-one mapping between device and sensor measurements
	sensor_data = arduino_instance.takeMeasurement()
	for (measurement, value) in sensor_data.items():
		parameters['SensorData'][measurement] = []

	# Delay before applying voltage (can be used in AutoStaticBias to hold the device grounded between runs)
	if(parameters['StaticBias']['delayBeforeApplyingVoltage'] > 0):
		time.sleep(parameters['StaticBias']['delayBeforeApplyingVoltage'])

	smu_instance.rampDrainVoltageTo(parameters['StaticBias']['drainVoltageSetPoint'])
	smu_instance.rampGateVoltageTo(parameters['StaticBias']['gateVoltageSetPoint'])

	# Delay before measurements begin (only useful for allowing current to settle a little, not usually necessary)
	if(parameters['StaticBias']['delayBeforeMeasurementsBegin'] > 0):
		time.sleep(parameters['StaticBias']['delayBeforeMeasurementsBegin'])

	# RUN TEST
	results = runStaticBias(smu_instance, 
							arduino_instance,
							parameters['StaticBias']['drainVoltageSetPoint'],
							parameters['StaticBias']['gateVoltageSetPoint'],
							parameters['StaticBias']['totalBiasTime'], 
							parameters['StaticBias']['measurementTime'])

	smu_instance.rampGateVoltageTo(parameters['StaticBias']['gateVoltageWhenDone'])
	smu_instance.rampDrainVoltageTo(parameters['StaticBias']['drainVoltageWhenDone'])

	# Copy parameters and add in the test results
	jsonData = dict(parameters)
	jsonData['Results'] = results
	
	# Save results as a JSON object
	if(isSavingResults):
		dlu.saveJSON(parameters['deviceDirectory'], parameters['StaticBias']['saveFileName'], jsonData)
	
	# Show plots to the user
	if(isPlottingResults):
		dpu.plotJSON(jsonData, parameters, 'b')
		dpu.show()
	
	return jsonData

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
		'vds_data':vds_data,
		'id_data':id_data,
		'vgs_data':vgs_data,
		'ig_data':ig_data,
		'timestamps':timestamps
	}


