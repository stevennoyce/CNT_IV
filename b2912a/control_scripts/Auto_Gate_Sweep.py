# === Imports ===
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

	runAutoGateSweep(parameters, smu_instance, arduino_instance, gateSweepParameters, staticBiasParameters)	

def runAutoGateSweep(parameters, smu_instance, arduino_instance, gateSweepParameters, staticBiasParameters):
	numberOfSweeps = parameters['AutoGateSweep']['numberOfSweeps']

	# === START ===
	for i in range(numberOfSweeps):
		print('Starting sweep #'+str(i+1)+' of '+str(numberOfStaticBiases))

		# Run GateSweep, StaticBias (if desired)
		gateSweepScript.run(gateSweepParameters, smu_instance, isSavingResults=True, isPlottingResults=False)
		if(parameters['AutoGateSweep']['applyStaticBiasBetweenSweeps']):
			staticBiasScript.run(staticBiasParameters, smu_instance, arduino_instance, isSavingResults=True, isPlottingResults=False)
		
		print('Completed sweep #'+str(i+1)+' of '+str(numberOfSweeps))