# === Imports ===
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
	deviceHistoryParameters['DeviceHistory']['plotGateSweeps'] = True
	deviceHistoryParameters['DeviceHistory']['plotBurnOuts'] = False
	deviceHistoryParameters['DeviceHistory']['plotStaticBias'] = parameters['AutoGateSweep']['applyStaticBiasBetweenSweeps']
	deviceHistoryParameters['DeviceHistory']['saveFiguresGenerated'] = True
	deviceHistoryParameters['DeviceHistory']['excludeDataBeforeJSONIndex'] = 0
	deviceHistoryParameters['DeviceHistory']['excludeDataAfterJSONIndex'] =  float('inf')
	deviceHistoryParameters['DeviceHistory']['excludeDataBeforeJSONExperimentNumber'] = parameters['startIndexes']['experimentNumber']
	deviceHistoryParameters['DeviceHistory']['excludeDataAfterJSONExperimentNumber'] =  parameters['startIndexes']['experimentNumber']

	runAutoGateSweep(parameters, smu_instance, arduino_instance, gateSweepParameters, staticBiasParameters, deviceHistoryParameters)	

def runAutoGateSweep(parameters, smu_instance, arduino_instance, gateSweepParameters, staticBiasParameters, deviceHistoryParameters):
	numberOfSweeps = parameters['AutoGateSweep']['numberOfSweeps']

	# === START ===
	for i in range(numberOfSweeps):
		print('Starting sweep #'+str(i+1)+' of '+str(numberOfStaticBiases))

		# Run GateSweep, StaticBias (if desired), and save plots with DeviceHistory
		gateSweepScript.run(gateSweepParameters, smu_instance, isSavingResults=True, isPlottingResults=False)
		if(parameters['AutoGateSweep']['applyStaticBiasBetweenSweeps']):
			staticBiasScript.run(staticBiasParameters, smu_instance, arduino_instance, isSavingResults=True, isPlottingResults=False)
		deviceHistoryScript.run(deviceHistoryParameters, showFigures=False)
		
		print('Completed sweep #'+str(i+1)+' of '+str(numberOfSweeps))

