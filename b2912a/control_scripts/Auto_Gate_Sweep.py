# === Imports ===
from control_scripts import Gate_Sweep as gateSweepScript
from utilities import DataLoggerUtility as dlu


# === Main ===
def run(parameters, smu_instance, arduino_instance):
	# No setup required, just run
	runAutoGateSweep(parameters, smu_instance, arduino_instance)	

def runAutoGateSweep(parameters, smu_instance, arduino_instance):
	ags_parameters = parameters['runConfigs']['AutoGateSweep']

	numberOfSweeps = len(ags_parameters['drainVoltageSetPoints'])
	
	# === START ===
	for i in range(numberOfSweeps):
		print('Starting sweep #'+str(i+1)+' of '+str(numberOfSweeps))

		# Make copy of parameters to run GateSweep, but modify the Vds setpoint
		gateSweepParameters = dict(parameters)
		gateSweepParameters['runType'] = 'GateSweep'
		gateSweepParameters['runConfigs']['GateSweep']['drainVoltageSetPoint'] = ags_parameters['drainVoltageSetPoints'][i]
		
		gateSweepScript.run(gateSweepParameters, smu_instance, isSavingResults=True, isPlottingResults=False)
		
		print('Completed sweep #'+str(i+1)+' of '+str(numberOfSweeps))