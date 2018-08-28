# === Imports ===
import time
import numpy as np

from control_scripts import Device_History as deviceHistoryScript
from utilities import DataLoggerUtility as dlu



# === Main ===
def run(parameters, smu_systems, isSavingResults=True, isPlottingResults=False):
	# Create distinct parameters for plotting the results
	dh_parameters = {}
	dh_parameters['Identifiers'] = dict(parameters['Identifiers'])
	dh_parameters['dataFolder'] = parameters['dataFolder']
	dh_parameters['plotGateSweeps'] = False
	dh_parameters['plotBurnOuts'] = False
	dh_parameters['plotStaticBias'] = False
	dh_parameters['showFiguresGenerated'] = True
	dh_parameters['saveFiguresGenerated'] = False
	dh_parameters['excludeDataBeforeJSONExperimentNumber'] = parameters['startIndexes']['experimentNumber']
	dh_parameters['excludeDataAfterJSONExperimentNumber'] =  parameters['startIndexes']['experimentNumber']
	
	# Get shorthand name to easily refer to configuration parameters
	afm_parameters = parameters['runConfigs']['AFMControl']
	
	smu_device = smu_systems['deviceSMU']
	smu_secondary = smu_systems['secondarySMU']

	# Print the starting message
	print('Beginning AFM-assisted measurements.')

	# === START ===
	results = runAFM(smu_device, smu_secondary)					
	# === COMPLETE ===

	# Add important metrics from the run to the parameters for easy access later in ParametersHistory
	parameters['Computed'] = results['Computed']
	
	# Copy parameters and add in the test results
	jsonData = dict(parameters)
	jsonData['Results'] = results['Raw']
		
	# Save results as a JSON object
	if(isSavingResults):
		print('Saving JSON: ' + str(dlu.getDeviceDirectory(parameters)))
		dlu.saveJSON(dlu.getDeviceDirectory(parameters), afm_parameters['saveFileName'], jsonData)

	# Show plots to the user
	if(isPlottingResults):
		deviceHistoryScript.run(dh_parameters)
		
	return jsonData

# === Data Collection ===
def runAFM(smu_device, smu_secondary, complianceCurrent=1e-6, complianceVoltage=10, gateVoltageSetPoint=0, drainVoltageSetPoint=0):
	# Duke label 184553 is 'USB0::0x0957::0x8E18::MY51141244::INSTR' - use for device drain (CH1) and gate (CH2)
	# Duke Label 184554 is 'USB0::0x0957::0x8E18::MY51141241::INSTR' - use for AFM channels x (CH1) and y (CH2)
	
	# Device SMU data
	vds_data = []
	id_data = []
	vgs_data = []
	ig_data = []
	device_timestamps = []
	
	# Seconary SMU data
	smu2_v1_data = []
	smu2_i1_data = []
	smu2_v2_data = []
	smu2_i2_data = []
	smu2_timestamps = []

	# Set SMU source modes
	smu_device.setChannel1SourceMode("voltage")
	smu_device.setChannel2SourceMode("voltage")
	
	smu_secondary.setChannel1SourceMode("current")
	smu_secondary.setChannel2SourceMode("current")
	
	# Set SMU NPLC
	smu_device.setNPLC(1)
	smu_secondary.setNPLC(1)
	
	# Set SMU compliance
	smu_device.setComplianceCurrent(complianceCurrent)	
	smu_device.setComplianceVoltage(complianceVoltage)
	
	smu_device.setComplianceCurrent(complianceCurrent)	
	smu_device.setComplianceVoltage(complianceVoltage)	


	
	# Apply Vgs and Vds to the device
	smu_device.rampDrainVoltageTo(drainVoltageSetPoint)
	smu_device.rampGateVoltageTo(gateVoltageSetPoint)

	
	
	# Take measurements
	sleep_time1 = smu_device.startSweep(drainVoltageSetPoint, drainVoltageSetPoint, gateVoltageSetPoint, gateVoltageSetPoint, 100, triggerInterval=None)
	sleep_time2 = smu_secondary.startSweep(0, 0, 0, 0, 100, triggerInterval=None)
	
	#time.sleep(0)
	
	results_device = smu_device.endSweep()
	results_secondary = smu_secondary.endSweep()
	
	
	
	# Pick the data to save
	vds_data = results_device['Vds_data']
	id_data = results_device['Id_data']
	vgs_data = results_device['Vgs_data']
	ig_data = results_device['Ig_data']
	timestamps_device = results_device['timestamps']
	
	smu2_v1_data = results_secondary['Vds_data']
	smu2_i1_data = results_secondary['Id_data']
	smu2_v2_data = results_secondary['Vgs_data']
	smu2_i2_data = results_secondary['Ig_data']
	timestamps_smu2 = results_secondary['timestamps']

	return {
		'Raw':{
			'vds_data':vds_data,
			'id_data':id_data,
			'vgs_data':vgs_data,
			'ig_data':ig_data,
			'timestamps_device':timestamps_device,
			'smu2_v1_data':smu2_v1_data,
			'smu2_i1_data':smu2_i1_data,
			'smu2_v2_data':smu2_v2_data,
			'smu2_i2_data':smu2_i2_data,
			'timestamps_smu2':timestamps_smu2,
		},
		'Computed':{
			'metric that you care about':123456789
		}
	}


	