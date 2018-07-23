# === Imports ===
import random
import time

from control_scripts import Gate_Sweep as gateSweepScript
from control_scripts import Static_Bias as staticBiasScript
from utilities import DataLoggerUtility as dlu



# === Main ===
def run(parameters, smu_instance, arduino_instance):
	# Create distinct parameters for all scripts that could be run
	gateSweepParameters = dict(parameters)
	gateSweepParameters['runType'] = 'GateSweep'

	staticBiasParameters = dict(parameters)
	staticBiasParameters['runType'] = 'StaticBias'

	runAutoStaticBias(parameters, smu_instance, arduino_instance, gateSweepParameters, staticBiasParameters)	

def runAutoStaticBias(parameters, smu_instance, arduino_instance, gateSweepParameters, staticBiasParameters):
	sb_parameters = staticBiasParameters['runConfigs']['StaticBias']
	asb_parameters = parameters['runConfigs']['AutoStaticBias']

	numberOfStaticBiases = asb_parameters['numberOfStaticBiases']
	
	# Build arrays of all parameters that could change over the course of any given experiement
	gateVoltageSetPointList = [sb_parameters['gateVoltageSetPoint']]*numberOfStaticBiases
	drainVoltageSetPointList = [sb_parameters['drainVoltageSetPoint']]*numberOfStaticBiases
	gateVoltageWhenDoneList = [sb_parameters['gateVoltageWhenDone']]*numberOfStaticBiases
	drainVoltageWhenDoneList = [sb_parameters['drainVoltageWhenDone']]*numberOfStaticBiases
	delayBeforeApplyingVoltageList = [sb_parameters['delayBeforeApplyingVoltage']]*numberOfStaticBiases
	delayBeforeMeasurementsList = [sb_parameters['delayBeforeMeasurementsBegin']]*numberOfStaticBiases

	# Modify parameter arrays so that they increment there values as desired
	currentIncrementNumber = 1
	for i in range(numberOfStaticBiases):
		if(i >= asb_parameters['numberOfBiasesBetweenIncrements']*currentIncrementNumber):
			currentIncrementNumber += 1
		gateVoltageSetPointList[i] += asb_parameters['incrementStaticGateVoltage']*(currentIncrementNumber-1)
		drainVoltageSetPointList[i] += asb_parameters['incrementStaticDrainVoltage']*(currentIncrementNumber-1)
		gateVoltageWhenDoneList[i] += asb_parameters['incrementGateVoltageWhenDone']*(currentIncrementNumber-1)
		drainVoltageWhenDoneList[i] += asb_parameters['incrementDrainVoltageWhenDone']*(currentIncrementNumber-1)
		delayBeforeApplyingVoltageList[i] += asb_parameters['incrementDelayBeforeReapplyingVoltage']*(currentIncrementNumber-1)	
	delayBeforeMeasurementsList[0] = asb_parameters['firstDelayBeforeMeasurementsBegin']

	# Randomize the time spent grounding the terminals if desired
	if(asb_parameters['shuffleDelaysBeforeReapplyingVoltage']):
		random.shuffle(delayBeforeApplyingVoltageList)



	## === START ===
	print('Beginning AutoStaticBias test with the following parameter lists:')
	print(' Gate Voltages:  {:} \n Drain Voltages:  {:} \n Gate Voltages between biases:  {:} \n Drain Voltages between biases:  {:} \n Delay Between Applying Voltages:  {:} \n Delay Before Measurements Begin:  {:}'.format(gateVoltageSetPointList, drainVoltageSetPointList, gateVoltageWhenDoneList, drainVoltageWhenDoneList, delayBeforeApplyingVoltageList, delayBeforeMeasurementsList))
	
	# Run a pre-test gate sweep just to make sure everything looks good
	if(asb_parameters['doInitialGateSweep']):
		print('Taking an initial sweep to get a baseline of device performance prior to StaticBias...')
		gateSweepScript.run(gateSweepParameters, smu_instance, isSavingResults=True, isPlottingResults=False)

	# Run all Static Biases in this Experiment
	for i in range(numberOfStaticBiases):
		print('Starting static bias #'+str(i+1)+' of '+str(numberOfStaticBiases))
		
		# Get the parameters for this StaticBias from the pre-built arrays
		sb_parameters['gateVoltageSetPoint'] = gateVoltageSetPointList[i]
		sb_parameters['drainVoltageSetPoint'] = drainVoltageSetPointList[i]
		sb_parameters['gateVoltageWhenDone'] = gateVoltageWhenDoneList[i]
		sb_parameters['drainVoltageWhenDone'] = drainVoltageWhenDoneList[i]
		sb_parameters['delayBeforeApplyingVoltage'] = delayBeforeApplyingVoltageList[i]
		sb_parameters['delayBeforeMeasurementsBegin'] = delayBeforeMeasurementsList[i]
		
		# Run StaticBias, GateSweep (if desired)
		staticBiasScript.run(staticBiasParameters, smu_instance, arduino_instance, isSavingResults=True, isPlottingResults=False)
		if(asb_parameters['applyGateSweepBetweenBiases']):
			gateSweepScript.run(gateSweepParameters, smu_instance, isSavingResults=True, isPlottingResults=False)
		
		# Float the channels if desired
		if(asb_parameters['turnChannelsOffBetweenBiases']):
			print('Turning channels off for: ' + str(asb_parameters['channelsOffTime']) + ' seconds...')
			smu_instance.turnChannelsOff()
			time.sleep(asb_parameters['channelsOffTime'])
			smu_instance.turnChannelsOn()
			print('Channels are back on.')

		print('Completed static bias #'+str(i+1)+' of '+str(numberOfStaticBiases))
		



