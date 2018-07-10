import B2912A_Burn_Out as burnOutScript
import B2912A_Gate_Sweep as gateSweepScript
import Device_History as deviceHistoryScript
from utilities import DataLoggerUtility as dlu



# === Main ===
def run(parameters, smu_instance):
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

	sweepResults = gateSweepScript.run(gateSweepParameters, smu_instance, True, False)
	previousOnOffRatio = sweepResults['Results']['onOffRatio']

	while((previousOnOffRatio < targetOnOffRatio) and (burnOutCount < burnOutLimit)):
		burnOutScript.run(burnOutParameters, smu_instance, True, False)
		sweepResults = gateSweepScript.run(gateSweepParameters, smu_instance, True, False)

		currentOnOffRatio = sweepResults['Results']['onOffRatio']
		if(currentOnOffRatio < allowedDegradationFactor*previousOnOffRatio):
			break
		previousOnOffRatio = currentOnOffRatio

		deviceHistoryScript.run(deviceHistoryParameters, False)
		burnOutCount += 1
		print('Completed sweep #'+str(burnOutCount))
		
