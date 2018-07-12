# === Imports ===
from control_scripts import Burn_Out as burnOutScript
from control_scripts import Gate_Sweep as gateSweepScript
from control_scripts import Device_History as deviceHistoryScript
from utilities import DataLoggerUtility as dlu



# === Main ===
def run(parameters, smu_instance):
	# Create distinct parameters for all scripts that could be run
	gateSweepParameters = dict(parameters)
	gateSweepParameters['runType'] = 'GateSweep'

	burnOutParameters = dict(parameters)
	burnOutParameters['runType'] = 'BurnOut'
	
	deviceHistoryParameters = dict(parameters)
	deviceHistoryParameters['runType'] = 'DeviceHistory'
	deviceHistoryParameters['DeviceHistory']['plotGateSweeps'] = True
	deviceHistoryParameters['DeviceHistory']['plotBurnOuts'] = True
	deviceHistoryParameters['DeviceHistory']['plotStaticBias'] = False
	deviceHistoryParameters['DeviceHistory']['saveFiguresGenerated'] = True
	deviceHistoryParameters['DeviceHistory']['excludeDataBeforeJSONIndex'] = 0
	deviceHistoryParameters['DeviceHistory']['excludeDataAfterJSONIndex'] =  float('inf')
	deviceHistoryParameters['DeviceHistory']['excludeDataBeforeJSONExperimentNumber'] = parameters['startIndexes']['experimentNumber']
	deviceHistoryParameters['DeviceHistory']['excludeDataAfterJSONExperimentNumber'] =  parameters['startIndexes']['experimentNumber']
	deviceHistoryParameters['DeviceHistory']['showOnlySuccessfulBurns'] = False

	runAutoBurnOut(parameters, smu_instance, gateSweepParameters, burnOutParameters, deviceHistoryParameters)

def runAutoBurnOut(parameters, smu_instance, gateSweepParameters, burnOutParameters, deviceHistoryParameters):
	targetOnOffRatio = parameters['AutoBurnOut']['targetOnOffRatio']
	allowedDegradationFactor = parameters['AutoBurnOut']['limitOnOffRatioDegradation']
	burnOutLimit = parameters['AutoBurnOut']['limitBurnOutsAllowed']
	burnOutCount = 0

	# === START ===
	# Take an initial sweep to get a baseline for device performance
	sweepResults = gateSweepScript.run(gateSweepParameters, smu_instance, True, False)
	previousOnOffRatio = sweepResults['Results']['onOffRatio']

	while((previousOnOffRatio < targetOnOffRatio) and (burnOutCount < burnOutLimit)):
		print('Starting burnout #'+str(burnOutCount+1))

		# Run BurnOut and GateSweep
		burnOutScript.run(burnOutParameters, smu_instance, True, False)
		sweepResults = gateSweepScript.run(gateSweepParameters, smu_instance, True, False)

		# If the On/Off ratio dropped by more than 'allowedDegredationFactor' stop BurnOut now
		currentOnOffRatio = sweepResults['Results']['onOffRatio']
		if(currentOnOffRatio < allowedDegradationFactor*previousOnOffRatio):
			break
		previousOnOffRatio = currentOnOffRatio

		# Save plots with DeviceHistory
		deviceHistoryScript.run(deviceHistoryParameters, showFigures=False)
		
		print('Completed sweep #'+str(burnOutCount+1))
		burnOutCount += 1
		
