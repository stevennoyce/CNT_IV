import time
import numpy as np

from utilities import DataLoggerUtility as dlu
from utilities import DataPlotterUtility as dpu
from framework import SourceMeasureUnit as smu

# ## ********** Parameters **********

# default_parameters = {
# 	'runType':'StaticBias',
# 	'chipID':'C127-',
# 	'deviceID':'0-0',
# 	'NPLC':1,
# 	'time': 30,
# 	'complianceCurrent':	100e-6,
# 	'gateVoltageSetPoint':	-15.0,
# 	'drainVoltageSetPoint':	0.5,
# }

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

	smu_instance.rampDrainVoltageTo(parameters['StaticBias']['drainVoltageSetPoint'], steps=20)
	smu_instance.rampGateVoltageTo(parameters['StaticBias']['gateVoltageSetPoint'], steps=30)

	# Delay before measurements begin (only useful for allowing current to settle a little, not usually necessary)
	if(parameters['StaticBias']['delayBeforeMeasurementsBegin'] > 0):
		time.sleep(parameters['StaticBias']['delayBeforeMeasurementsBegin'])

	results = runStaticBias(smu_instance, 
							arduino_instance,
							parameters['StaticBias']['drainVoltageSetPoint'],
							parameters['StaticBias']['gateVoltageSetPoint'],
							parameters['StaticBias']['totalBiasTime'], 
							parameters['StaticBias']['measurementTime'])

	smu_instance.rampGateVoltageTo(parameters['StaticBias']['gateVoltageWhenDone'], steps=30)
	smu_instance.rampDrainVoltageTo(parameters['StaticBias']['drainVoltageWhenDone'], steps=20)

	jsonData = {**parameters, **results}
	
	if(isSavingResults):
		dlu.saveJSON(parameters['deviceDirectory'], parameters['StaticBias']['saveFileName'], jsonData)
	
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
	pointsToAverageOver = (measurementTime)*(smu_instance.measurementsPerSecond)/(smu_instance.nplc)
	
	

	for i in range(steps):
		measurements = smu_instance.takeSweep(drainVoltageSetPoint, drainVoltageSetPoint, gateVoltageSetPoint, gateVoltageSetPoint, pointsToAverageOver/1.5)
		timestamp = time.time()
		
		vds_data.append(np.median(measurements['Vds_data']))
		id_data.append(np.median(measurements['Id_data']))
		vgs_data.append(np.median(measurements['Vgs_data']))
		ig_data.append(np.median(measurements['Ig_data']))
		timestamps.append(timestamp)

		sensor_data = arduino_instance.takeMeasurement()
		for (measurement, value) in sensor_data.items():
			parameters['SensorData'][measurement].append(value)

		print('\r[' + int(i*70.0/steps)*'=' + (70-int(i*70.0/steps)-1)*' ' + ']', end='')
	print('')

	return {
		'voltage1s':vds_data,
		'current1s':id_data,
		'voltage2s':vgs_data,
		'current2s':ig_data,
		'timestamps':timestamps
	}



if __name__ == '__main__':
    run(default_parameters)