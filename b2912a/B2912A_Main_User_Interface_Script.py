import os
import time
import sys
import platform
import serial as pySerial

import B2912A_Burn_Out as burnOutScript
import B2912A_Gate_Sweep as gateSweepScript
import B2912A_Auto_Burn_Out as autoBurnScript
import B2912A_Static_Bias as staticBiasScript
import B2912A_Auto_Gate_Sweep as autoGateScript
import B2912A_Auto_Static_Bias as autoBiasScript
import Device_History as deviceHistoryScript
import Chip_History as chipHistoryScript

from utilities import DataLoggerUtility as dlu
from utilities import PlotPostingUtility as plotPoster
from framework import SourceMeasureUnit as smu
from framework import ArduinoBoard as arduinoBoard

def devicesInRange(startContact, endContact, skip=True):
	contactList = set(range(startContact,endContact))
	if(skip):
		omitList = set(range(4,64+1,4))
		contactList = list(contactList-omitList)
	return ['{0:}-{1:}'.format(c, c+1) for c in contactList]

## ********** Parameters **********

os.chdir(sys.path[0])
#sys.path.append('framework/')
#sys.path.append('utilities/')

if platform.node() == 'noyce-dell':
	chipID = 'C127X'
	deviceID = '15-16'
elif platform.node() == 'Steven-Noyce-MacBook-Pro.local':
	chipID = 'C127E'
	deviceID = '14-15'
	
	chipID = 'C127X'
	deviceID = '15-16'
	# Experiments 3 to 4
	# Experiment 57 - 
	# Experiment 65 - 

	chipID = 'C127E'
	deviceID = '15-16'
	# Experiment 6 to 6, many decay curves and subthreshold curves
	# Separate plot, index 11 to 12, one decay curve
	# Separate plot, index 13 to 21, four decay curves
	# Separate plot, index 17 to 18, decent subthreshold curve with error bars
	# Separate plot, experiments 3 to 18, decaying subthreshold curves
	# Separate plot, experiments 3 to 13, stable/slowly decreasing subthreshold and transfer and on/off curves
	
	# chipID = 'C127P'
	# deviceID = '1-2'
	# # Experiment 8 to 8
	
	chipID = 'C134K'
	deviceID = '15-16'
else:
	chipID = 'C127X'
	deviceID = '15-16'

runTypes = {
	0:'Quit',
	1:'GateSweep',
	2:'BurnOut',
	3:'AutoBurnOut',
	4:'StaticBias',
	5:'AutoGateSweep',
	6:'AutoStaticBias',
	7:'DeviceHistory',
	8:'ChipHistory'
}

default_parameters = {
	'ParametersFormatVersion': 2,
	'GateSweep':{
		'saveFileName': 'GateSweep',
		'isFastSweep': False,
		'isAlternatingSweep': False,
		'pulsedMeasurementOnTime': 0,
		'pulsedMeasurementOffTime': 0,
		'stepsInVGSPerDirection': 50,
		'pointsPerVGS': 1,
		'complianceCurrent':	100e-6,
		'drainVoltageSetPoint':	-0.1,
		'gateVoltageMinimum':	-3,
		'gateVoltageMaximum': 	3
	},
	'BurnOut':{
		'saveFileName': 'BurnOut',
		'pointsPerRamp': 50,
		'pointsPerHold': 50,
		'complianceCurrent':	2e-3,
		'thresholdProportion':	0.8,
		'minimumAppliedDrainVoltage': 0.9,
		'gateVoltageSetPoint':	15.0,
		'drainVoltageMaxPoint':	10,
		'drainVoltagePlateaus': 10
	},
	'AutoBurnOut':{
		'targetOnOffRatio': 300,
		'limitBurnOutsAllowed': 8,
		'limitOnOffRatioDegradation': 0.7
	},
	'StaticBias':{
		'saveFileName': 'StaticBias',
		'totalBiasTime': 60*60,
		'measurementTime': 10,
		'complianceCurrent': 100e-6,
		'delayBeforeApplyingVoltage': 0,
		'delayBeforeMeasurementsBegin': 0,
		'gateVoltageSetPoint': 	15,
		'drainVoltageSetPoint':	-0.5,
		'gateVoltageWhenDone':  0,
		'drainVoltageWhenDone': 0
	},
	'AutoGateSweep':{
		'numberOfSweeps': 3,
		'applyStaticBiasBetweenSweeps': False,
	},
	'AutoStaticBias':{
		'numberOfStaticBiases': 2,
		'applyGateSweepBetweenBiases': True,
		'firstDelayBeforeMeasurementsBegin': 0,
		'numberOfBiasesBetweenIncrements': 1,
		'incrementStaticGateVoltage':  -30,
		'incrementStaticDrainVoltage': 0,
		'incrementGateVoltageWhenDone': 0,
		'incrementDrainVoltageWhenDone': 0,
		'incrementDelayBeforeReapplyingVoltage': 0,
		'shuffleDelaysBeforeReapplyingVoltage': False
	},
	'DeviceHistory':{
		'showFiguresGenerated': True,
		'saveFiguresGenerated': True,
		'postFiguresGenerated': False,
		'plotGateSweeps': True,
		'plotBurnOuts':   False,
		'plotStaticBias': False,
		'excludeDataBeforeJSONIndex': 0,
		'excludeDataAfterJSONIndex':  float('inf'),
		'excludeDataBeforeJSONExperimentNumber': 55,
		'excludeDataAfterJSONExperimentNumber':  55,
		'gateSweepDirection': ['both','forward','reverse'][2],
		'showOnlySuccessfulBurns': False,
		'timescale': ['','seconds','minutes','hours','days','weeks'][0],
		'plotInRealTime': True,
		'includeBiasVoltageSubplot': False
	},
	'ChipHistory':{
		
	},
	'Results':{

	},
	'SensorData':{

	},
	'MeasurementSystem':['B2912A','PCB2v14'][0],
	'chipID':chipID,
	'deviceID':deviceID,
	'deviceRange':[],#devicesInRange(2,32,skip=False),
	'dataFolder':'data/',
	'plotsFolder':'CurrentPlots/',
	'postFigures':	True,
	'NPLC':1
}

def main(parameters):
	while(True):
		os.system('cls' if os.name == 'nt' else 'clear')

		# Get user's action selection
		choice = int(selectFromDictionary('Actions: ', runTypes, 'Choose an action (0,1,2,...): '))
		if(choice == 0):
			break

		# Allow user to confirm the parameters before continuing
		parameters = dict(default_parameters)
		parameters['runType'] = runTypes[choice]
		confirmation = str(selectFromDictionary('Parameters: ', parameters, 'Are parameters correct? (y/n): '))
		if(confirmation != 'y'):
			break

		# Initialize measurement system
		smu_instance = initSMU(parameters)		

		# Initialize Arduino connection
		arduino_instance = initArduino(parameters)
		print("Sensor data: " + str(parameters['SensorData']))


		
		# Run specified action:
		if((parameters['MeasurementSystem'] == 'PCB2v14') and (len(parameters['deviceRange']) > 0) and (parameters['runType'] not in ['DeviceHistory', 'ChipHistory'])):
			for device in parameters['deviceRange']:
				parameters = dict(default_parameters)
				parameters['runType'] = runTypes[choice]
				parameters['deviceID'] = device
				runAction(parameters, smu_instance)
		else:
			runAction(parameters, smu_instance)
		
		break

# Run generic user action
def runAction(parameters, smu_instance):
	parameters['deviceDirectory'] = parameters['dataFolder'] + parameters['chipID'] + '/' + parameters['deviceID'] + '/'	
	dlu.makeFolder(parameters['deviceDirectory'])
	dlu.makeFolder(parameters['plotsFolder'])
	dlu.emptyFolder(parameters['plotsFolder'])

	if(parameters['runType'] == 'DeviceHistory'):
		runDeviceHistory(parameters)
	elif(parameters['runType'] == 'ChipHistory'):
		chipHistoryScript.run(parameters)
	else:
		runSMU(parameters, smu_instance)

# Run an action that interfaces with the SMU.
def runSMU(parameters, smu_instance):
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
	
	deviceHistoryScript.run(parameters, showFigures=parameters['DeviceHistory']['showFiguresGenerated'])
	
	if(parameters['DeviceHistory']['postFiguresGenerated']):
		plotPoster.postPlots(parameters)





# *** SMU Connection ***

# Get a connection to the SMU specified in parameters.
def initSMU(parameters):
	smu_instance = None
	if(parameters['runType'] not in ['DeviceHistory', 'ChipHistory']):
		if(parameters['MeasurementSystem'] == 'B2912A'):
			smu_instance = smu.getConnectionFromVisa(parameters['NPLC'], defaultComplianceCurrent=100e-6, smuTimeout=60000)
		elif(parameters['MeasurementSystem'] == 'PCB2v14'):
			smu_instance = smu.getConnectionToPCB()
		else:
			raise NotImplementedError("Unkown Measurement System specified (try B2912A, PCB2v14, ...)")
	print("Connected to SMU: " + str(parameters['MeasurementSystem']))
	return smu_instance



# *** Arduino Connection ***
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
	


# *** User Interface ***

# Present a dictionary of options to the user and get their choice.
def selectFromDictionary(titleString, dictionary, promptString):
	print(titleString)
	print_dict(dictionary, 0)
	return input(promptString)

# Print a nicely formatted dictionary.
def print_dict(dictionary, numtabs):
	keys = list(dictionary.keys())
	for i in range(len(keys)):
		if(isinstance(dictionary[keys[i]], dict)):
			print(" '" + str(keys[i])+ "': {")
			print_dict(dictionary[keys[i]], numtabs+1)
		else:
			print(numtabs*'\t'+'  ' + str(keys[i]) + ': ' + str(dictionary[keys[i]]))




if __name__ == '__main__':
    main(default_parameters)

