# === Imports ===
import random
import time

from control_scripts import Gate_Sweep as gateSweepScript
from control_scripts import Static_Bias as staticBiasScript
from control_scripts import Device_History as deviceHistoryScript
from utilities import DataLoggerUtility as dlu



# === Main ===
def run(parameters, smu_instance, arduino_instance):
	# Create distinct parameters for all scripts that could be run
	gateSweepParameters = dict(parameters)
	gateSweepParameters['runType'] = 'GateSweep'

	staticBiasParameters = dict(parameters)
	staticBiasParameters['runType'] = 'StaticBias'
	
	deviceHistoryParameters = dict(parameters)
	deviceHistoryParameters['runType'] = 'DeviceHistory'
	deviceHistoryParameters['DeviceHistory']['plotGateSweeps'] = parameters['AutoStaticBias']['applyGateSweepBetweenBiases']
	deviceHistoryParameters['DeviceHistory']['plotBurnOuts'] = False
	deviceHistoryParameters['DeviceHistory']['plotStaticBias'] = True
	deviceHistoryParameters['DeviceHistory']['saveFiguresGenerated'] = True
	deviceHistoryParameters['DeviceHistory']['excludeDataBeforeJSONIndex'] = 0
	deviceHistoryParameters['DeviceHistory']['excludeDataAfterJSONIndex'] =  float('inf')
	deviceHistoryParameters['DeviceHistory']['excludeDataBeforeJSONExperimentNumber'] = parameters['startIndexes']['experimentNumber']
	deviceHistoryParameters['DeviceHistory']['excludeDataAfterJSONExperimentNumber'] =  parameters['startIndexes']['experimentNumber']

	runAutoStaticBias(parameters, smu_instance, arduino_instance, gateSweepParameters, staticBiasParameters, deviceHistoryParameters)	

def runAutoStaticBias(parameters, smu_instance, arduino_instance, gateSweepParameters, staticBiasParameters, deviceHistoryParameters):
	numberOfStaticBiases = parameters['AutoStaticBias']['numberOfStaticBiases']
	
	# Build arrays of all parameters that could change over the course of any given experiement
	gateVoltageSetPointList = [staticBiasParameters['StaticBias']['gateVoltageSetPoint']]*numberOfStaticBiases
	drainVoltageSetPointList = [staticBiasParameters['StaticBias']['drainVoltageSetPoint']]*numberOfStaticBiases
	gateVoltageWhenDoneList = [staticBiasParameters['StaticBias']['gateVoltageWhenDone']]*numberOfStaticBiases
	drainVoltageWhenDoneList = [staticBiasParameters['StaticBias']['drainVoltageWhenDone']]*numberOfStaticBiases
	delayBeforeApplyingVoltageList = [staticBiasParameters['StaticBias']['delayBeforeApplyingVoltage']]*numberOfStaticBiases
	delayBeforeMeasurementsList = [staticBiasParameters['StaticBias']['delayBeforeMeasurementsBegin']]*numberOfStaticBiases

	# Modify parameter arrays so that they increment there values as desired
	currentIncrementNumber = 1
	for i in range(numberOfStaticBiases):
		if(i >= parameters['AutoStaticBias']['numberOfBiasesBetweenIncrements']*currentIncrementNumber):
			currentIncrementNumber += 1
		gateVoltageSetPointList[i] += parameters['AutoStaticBias']['incrementStaticGateVoltage']*(currentIncrementNumber-1)
		drainVoltageSetPointList[i] += parameters['AutoStaticBias']['incrementStaticDrainVoltage']*(currentIncrementNumber-1)
		gateVoltageWhenDoneList[i] += parameters['AutoStaticBias']['incrementGateVoltageWhenDone']*(currentIncrementNumber-1)
		drainVoltageWhenDoneList[i] += parameters['AutoStaticBias']['incrementDrainVoltageWhenDone']*(currentIncrementNumber-1)
		delayBeforeApplyingVoltageList[i] += parameters['AutoStaticBias']['incrementDelayBeforeReapplyingVoltage']*(currentIncrementNumber-1)	
	delayBeforeMeasurementsList[0] = parameters['AutoStaticBias']['firstDelayBeforeMeasurementsBegin']

	# Randomize the time spent grounding the terminals if desired
	if(parameters['AutoStaticBias']['shuffleDelaysBeforeReapplyingVoltage']):
		random.shuffle(delayBeforeApplyingVoltageList)



	## === START ===
	print('Beginning AutoStaticBias test with the following parameter lists:')
	print(' Gate Voltages:  {:} \n Drain Voltages:  {:} \n Gate Voltages between biases:  {:} \n Drain Voltages between biases:  {:} \n Delay Between Applying Voltages:  {:} \n Delay Before Measurements Begin:  {:}'.format(gateVoltageSetPointList, drainVoltageSetPointList, gateVoltageWhenDoneList, drainVoltageWhenDoneList, delayBeforeApplyingVoltageList, delayBeforeMeasurementsList))
	
	# Run a pre-test gate sweep just to make sure everything looks good
	gateSweepScript.run(gateSweepParameters, smu_instance, isSavingResults=True, isPlottingResults=False)

	# Run all Static Biases in this Experiment
	for i in range(numberOfStaticBiases):
		print('Starting static bias #'+str(i+1)+' of '+str(numberOfStaticBiases))
		
		# Get the parameters for this StaticBias from the pre-built arrays
		staticBiasParameters['StaticBias']['gateVoltageSetPoint'] = gateVoltageSetPointList[i]
		staticBiasParameters['StaticBias']['drainVoltageSetPoint'] = drainVoltageSetPointList[i]
		staticBiasParameters['StaticBias']['gateVoltageWhenDone'] = gateVoltageWhenDoneList[i]
		staticBiasParameters['StaticBias']['drainVoltageWhenDone'] = drainVoltageWhenDoneList[i]
		staticBiasParameters['StaticBias']['delayBeforeApplyingVoltage'] = delayBeforeApplyingVoltageList[i]
		staticBiasParameters['StaticBias']['delayBeforeMeasurementsBegin'] = delayBeforeMeasurementsList[i]
		
		# Run StaticBias, GateSweep (if desired)
		staticBiasScript.run(staticBiasParameters, smu_instance, arduino_instance, isSavingResults=True, isPlottingResults=False)
		if(parameters['AutoStaticBias']['applyGateSweepBetweenBiases']):
			gateSweepScript.run(gateSweepParameters, smu_instance, isSavingResults=True, isPlottingResults=False)
		
		# Float the channels if desired
		if(parameters['AutoStaticBias']['turnChannelsOffBetweenBiases']):
			smu_instance.turnChannelsOff()
			time.sleep(parameters['AutoStaticBias']['channelsOffTime'])
			smu_instance.turnChannelsOn()
		
		# Save plots with DeviceHistory
		deviceHistoryScript.run(deviceHistoryParameters, showFigures=False)

		print('Completed static bias #'+str(i+1)+' of '+str(numberOfStaticBiases))
		



