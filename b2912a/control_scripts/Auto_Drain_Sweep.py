# === Imports ===
from control_scripts import Drain_Sweep as drainSweepScript
from utilities import DataLoggerUtility as dlu


# === Main ===
def run(parameters, smu_instance, arduino_instance):
	# No setup required, just run
	runAutoDrainSweep(parameters, smu_instance, arduino_instance)	

def runAutoDrainSweep(parameters, smu_instance, arduino_instance):
	ads_parameters = parameters['runConfigs']['AutoDrainSweep']

	numberOfSweeps = len(ads_parameters['gateVoltageSetPoints'])
	
	# === START ===
	for i in range(numberOfSweeps):
		print('Starting sweep #'+str(i+1)+' of '+str(numberOfSweeps))

		# Make copy of parameters to run GateSweep, but modify the Vds setpoint
		drainSweepParameters = dict(parameters)
		drainSweepParameters['runType'] = 'DrainSweep'
		drainSweepParameters['runConfigs']['DrainSweep']['gateVoltageSetPoint'] = ads_parameters['gateVoltageSetPoints'][i]
		
		drainSweepScript.run(drainSweepParameters, smu_instance, isSavingResults=True, isPlottingResults=False)
		
		print('Completed sweep #'+str(i+1)+' of '+str(numberOfSweeps))