# === Imports ===
import os
import sys
import platform
import time
import copy

from control_scripts import Burn_Out as burnOutScript
from control_scripts import Gate_Sweep as gateSweepScript
from control_scripts import Auto_Burn_Out as autoBurnScript
from control_scripts import Static_Bias as staticBiasScript
from control_scripts import Auto_Gate_Sweep as autoGateScript
from control_scripts import Auto_Static_Bias as autoBiasScript
from control_scripts import Device_History as deviceHistoryScript
from control_scripts import Chip_History as chipHistoryScript

from utilities import DataLoggerUtility as dlu
from utilities import PlotPostingUtility as plotPoster
from framework import SourceMeasureUnit as smu
from framework import ArduinoBoard as arduinoBoard

import defaults



# === Main API ===
def run(additional_parameters):
	parameters = defaults.with_added(additional_parameters)

	# Initialize measurement system
	smu_instance = initSMU(parameters)		

	# Initialize Arduino connection
	arduino_instance = initArduino(parameters)
	print("Sensor data: " + str(parameters['SensorData']))
	
	# Run specified action:
	if((parameters['MeasurementSystem']['system'] == 'PCB2v14') and (len(parameters['MeasurementSystem']['deviceRange']) > 0) and (parameters['runType'] not in ['DeviceHistory', 'ChipHistory'])):
		for device in parameters['MeasurementSystem']['deviceRange']:
			params = copy.deepcopy(parameters)
			params['Identifiers']['device'] = device
			runAction(params, smu_instance, arduino_instance)
	else:
		runAction(parameters, smu_instance, arduino_instance)



# === Internal API ===
# Run generic user action
def runAction(parameters, smu_instance, arduino_instance):
	print('Creating save folder.')
	dlu.makeFolder(dlu.getDeviceDirectory(parameters))

	if(parameters['runType'] == 'DeviceHistory'):
		runDeviceHistory(parameters)
	elif(parameters['runType'] == 'ChipHistory'):
		chipHistoryScript.run(parameters)
	else:
		runSMU(parameters, smu_instance, arduino_instance)

# Run an action that interfaces with the SMU.
def runSMU(parameters, smu_instance, arduino_instance):
	experiment = dlu.incrementJSONExperiementNumber(dlu.getDeviceDirectory(parameters))
	print('About to begin experiment #' + str(experiment))
	parameters['startIndexes'] = dlu.loadJSONIndex(dlu.getDeviceDirectory(parameters))
	parameters['startIndexes']['timestamp'] = time.time()

	smu_instance.setDevice(parameters['Identifiers']['device'])

	try:
		if(parameters['runType'] == 'GateSweep'):
			gateSweepScript.run(parameters, smu_instance)
		elif(parameters['runType'] == 'BurnOut'):
			burnOutScript.run(parameters, smu_instance)
		elif(parameters['runType'] == 'AutoBurnOut'):
			autoBurnScript.run(parameters, smu_instance)
		elif(parameters['runType'] == 'StaticBias'):
			staticBiasScript.run(parameters, smu_instance, arduino_instance)
		elif(parameters['runType'] == 'AutoGateSweep'):
			autoGateScript.run(parameters, smu_instance, arduino_instance)
		elif(parameters['runType'] == 'AutoStaticBias'):
			autoBiasScript.run(parameters, smu_instance, arduino_instance)
		else:
			raise NotImplementedError("Invalid action for the Source Measure Unit")
	except Exception as e:
		smu_instance.rampDownVoltages()

		parameters['endIndexes'] = dlu.loadJSONIndex(dlu.getDeviceDirectory(parameters))
		parameters['endIndexes']['timestamp'] = time.time()
		print('Saving to ParametersHistory...')
		dlu.saveJSON(dlu.getDeviceDirectory(parameters), 'ParametersHistory', parameters, incrementIndex=False)

		print('ERROR: Exception raised during the experiment.')
		raise

	smu_instance.rampDownVoltages()
	parameters['endIndexes'] = dlu.loadJSONIndex(dlu.getDeviceDirectory(parameters))
	parameters['endIndexes']['timestamp'] = time.time()

	print('Saving to ParametersHistory...')
	dlu.saveJSON(dlu.getDeviceDirectory(parameters), 'ParametersHistory', parameters, incrementIndex=False)

	#print('Posting plots online...')
	#plotPoster.postPlots(parameters)

# Run a "Device History" action.
def runDeviceHistory(parameters):
	dh_parameters = {
		'Identifiers': dict(parameters['Identifiers'])
		'dataFolder': parameters['dataFolder']
	}
	if('DeviceHistory' in parameters.keys()):
		dh_parameters.update(parameters['DeviceHistory'])

	print('Launching DeviceHistory.')
	deviceHistoryScript.run(dh_parameters)



# === SMU Connection ===
def initSMU(parameters):
	smu_instance = None
	if(parameters['runType'] not in ['DeviceHistory', 'ChipHistory']):
		if(parameters['MeasurementSystem']['system'] == 'B2912A'):
			smu_instance = smu.getConnectionFromVisa(parameters['MeasurementSystem']['NPLC'], defaultComplianceCurrent=100e-6, smuTimeout=60*1000)
		elif(parameters['MeasurementSystem']['system'] == 'PCB2v14'):
			smu_instance = smu.getConnectionToPCB()
		else:
			raise NotImplementedError("Unkown Measurement System specified (try B2912A, PCB2v14, ...)")
		print("Connected to SMU: " + str(parameters['MeasurementSystem']['system']))
	return smu_instance



# === Arduino Connection ===
def initArduino(parameters):
	arduino_instance = None
	baud = 9600
	try:
		port = '/dev/cu.wchusbserial1410'
		arduino_instance = arduinoBoard.getConnection(port, baud)
		print("Connected to Arduino on port: " + str(port))
	except: 
		try:
			port = '/dev/cu.wchusbserial1420'
			arduino_instance = arduinoBoard.getConnection(port, baud)
			print("Connected to Arduino on port: " + str(port))
		except: 
			print("No Arduino connected.")
			return arduinoBoard.getNullInstance()
	sensor_data = arduino_instance.takeMeasurement()
	for (measurement, value) in sensor_data.items():
		parameters['SensorData'][measurement] = [value]
	return arduino_instance
	


