import random

import B2912A_Gate_Sweep as gateSweepScript
import B2912A_Static_Bias as staticBiasScript
import Device_History as deviceHistoryScript
from utilities import DataLoggerUtility as dlu



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

	if(parameters['AutoStaticBias']['shuffleDelaysBeforeReapplyingVoltage']):
		random.shuffle(delayBeforeApplyingVoltageList)

	print('Beginning AutoStaticBias test with the following parameter lists:')
	print(' Gate Voltages:  {:} \n Drain Voltages:  {:} \n Delay Between Applying Voltages:  {:} \n Delay Before Measurements Begin:  {:}'.format(gateVoltageSetPointList, drainVoltageSetPointList, delayBeforeApplyingVoltageList, delayBeforeMeasurementsList))
	
	# Run all Tests in this Experiment
	for i in range(numberOfStaticBiases):
		print('Starting static bias #'+str(i+1)+' of '+str(numberOfStaticBiases))
		
		staticBiasParameters['StaticBias']['gateVoltageSetPoint'] = gateVoltageSetPointList[i]
		staticBiasParameters['StaticBias']['drainVoltageSetPoint'] = drainVoltageSetPointList[i]
		staticBiasParameters['StaticBias']['gateVoltageWhenDone'] = gateVoltageWhenDoneList[i]
		staticBiasParameters['StaticBias']['drainVoltageWhenDone'] = drainVoltageWhenDoneList[i]
		staticBiasParameters['StaticBias']['delayBeforeApplyingVoltage'] = delayBeforeApplyingVoltageList[i]
		staticBiasParameters['StaticBias']['delayBeforeMeasurementsBegin'] = delayBeforeMeasurementsList[i]

		# Run StaticBias, GateSweep (if necessary), and save plots with DeviceHistory
		staticBiasScript.run(staticBiasParameters, smu_instance, arduino_instance, isSavingResults=True, isPlottingResults=False)
		if(parameters['AutoStaticBias']['applyGateSweepBetweenBiases']):
			gateSweepScript.run(gateSweepParameters, smu_instance, isSavingResults=True, isPlottingResults=False)
		deviceHistoryScript.run(deviceHistoryParameters, showFigures=False)

		print('Completed static bias #'+str(i+1)+' of '+str(numberOfStaticBiases))
		



