import os
import sys
import platform

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



# === Main API ===
def run(parameters):
	# Define the working directory for saving all device data
	parameters['deviceDirectory'] = os.path.join(parameters['dataFolder'], parameters['waferID'], parameters['chipID'], parameters['deviceID']) + '/'

	# Initialize measurement system
	smu_instance = initSMU(parameters)		

	# Initialize Arduino connection
	arduino_instance = initArduino(parameters)
	print("Sensor data: " + str(parameters['SensorData']))
	
	# Run specified action:
	if((parameters['MeasurementSystem'] == 'PCB2v14') and (len(parameters['deviceRange']) > 0) and (parameters['runType'] not in ['DeviceHistory', 'ChipHistory'])):
		for device in parameters['deviceRange']:
			params = dict(parameters)
			params['deviceID'] = device
			runAction(params, smu_instance, arduino_instance)
	else:
		runAction(parameters, smu_instance, arduino_instance)



# === Internal API ===
# Run generic user action
def runAction(parameters, smu_instance, arduino_instance):
	dlu.makeFolder(parameters['deviceDirectory'])
	dlu.makeFolder(parameters['plotsFolder'])
	dlu.emptyFolder(parameters['plotsFolder'])

	if(parameters['runType'] == 'DeviceHistory'):
		runDeviceHistory(parameters)
	elif(parameters['runType'] == 'ChipHistory'):
		chipHistoryScript.run(parameters)
	else:
		runSMU(parameters, smu_instance, arduino_instance)

# Run an action that interfaces with the SMU.
def runSMU(parameters, smu_instance, arduino_instance):
	dlu.incrementJSONExperiementNumber(parameters['deviceDirectory'])
	parameters['startIndexes'] = dlu.loadJSONIndex(parameters['deviceDirectory'])	
	smu_instance.setDevice(parameters['deviceID'])

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
	except:
		smu_instance.rampDownVoltages()
		choice = str(input('An error occurred. Quit and display error? (y/n):'))
		if(choice == 'y'):
			raise

	smu_instance.rampDownVoltages()
	parameters['endIndexes'] = dlu.loadJSONIndex(parameters['deviceDirectory'])
	dlu.saveJSON(parameters['deviceDirectory'], 'ParametersHistory', parameters, incrementIndex=False)
	plotPoster.postPlots(parameters)

# Run a "Device History" action.
def runDeviceHistory(parameters):
	parameters['startIndexes'] = {
		'index': parameters['DeviceHistory']['excludeDataBeforeJSONIndex'],
		'experimentNumber': parameters['DeviceHistory']['excludeDataBeforeJSONExperimentNumber']
	}
	parameters['endIndexes'] = {
		'index': min(parameters['DeviceHistory']['excludeDataBeforeJSONIndex'], dlu.loadJSONIndex(parameters['deviceDirectory'])['index']),
		'experimentNumber': min(parameters['DeviceHistory']['excludeDataBeforeJSONExperimentNumber'], dlu.loadJSONIndex(parameters['deviceDirectory'])['experimentNumber'])
	} 
	
	plotList = deviceHistoryScript.run(parameters, showFigures=parameters['DeviceHistory']['showFiguresGenerated'])
	
	if(parameters['DeviceHistory']['postFiguresGenerated']):
		plotPoster.postPlots(parameters)

	return plotList



# === SMU Connection ===
def initSMU(parameters):
	smu_instance = None
	if(parameters['runType'] not in ['DeviceHistory', 'ChipHistory']):
		if(parameters['MeasurementSystem'] == 'B2912A'):
			smu_instance = smu.getConnectionFromVisa(parameters['NPLC'], defaultComplianceCurrent=100e-6, smuTimeout=60*1000)
		elif(parameters['MeasurementSystem'] == 'PCB2v14'):
			smu_instance = smu.getConnectionToPCB()
		else:
			raise NotImplementedError("Unkown Measurement System specified (try B2912A, PCB2v14, ...)")
		print("Connected to SMU: " + str(parameters['MeasurementSystem']))
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
	


