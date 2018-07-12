# === Imports ===
import time
import numpy as np

from control_scripts import Device_History as deviceHistoryScript
from utilities import DataLoggerUtility as dlu
from utilities import DataGeneratorUtility as dgu
from utilities import DataPlotterUtility as dpu
#from framework import SourceMeasureUnit as smu



# === Main ===
def run(parameters, smu_instance, isSavingResults=True, isPlottingResults=True):
	# Create distinct parameters for plotting the results
	deviceHistoryParameters = dict(parameters)
	deviceHistoryParameters['runType'] = 'DeviceHistory'
	deviceHistoryParameters['DeviceHistory']['plotGateSweeps'] = True
	deviceHistoryParameters['DeviceHistory']['plotBurnOuts'] = False
	deviceHistoryParameters['DeviceHistory']['plotStaticBias'] = False
	deviceHistoryParameters['DeviceHistory']['saveFiguresGenerated'] = True
	deviceHistoryParameters['DeviceHistory']['excludeDataBeforeJSONIndex'] = 0
	deviceHistoryParameters['DeviceHistory']['excludeDataAfterJSONIndex'] =  float('inf')
	deviceHistoryParameters['DeviceHistory']['excludeDataBeforeJSONExperimentNumber'] = parameters['startIndexes']['experimentNumber']
	deviceHistoryParameters['DeviceHistory']['excludeDataAfterJSONExperimentNumber'] =  parameters['startIndexes']['experimentNumber']

	print('Sweeping the gate: V_DS='+str(parameters['GateSweep']['drainVoltageSetPoint'])+'V, min V_GS='+str(parameters['GateSweep']['gateVoltageMinimum'])+'V, max V_GS='+str(parameters['GateSweep']['gateVoltageMaximum'])+'V')
	smu_instance.setComplianceCurrent(parameters['GateSweep']['complianceCurrent'])	

	# === START ===
	smu_instance.rampDrainVoltageTo(parameters['GateSweep']['drainVoltageSetPoint'])
	results = runGateSweep( smu_instance, 
							isFastSweep=parameters['GateSweep']['isFastSweep'],
							isAlternatingSweep=parameters['GateSweep']['isAlternatingSweep'],
							pulsedMeasurementOnTime=parameters['GateSweep']['pulsedMeasurementOnTime'],
							pulsedMeasurementOffTime=parameters['GateSweep']['pulsedMeasurementOffTime'],
							drainVoltageSetPoint=parameters['GateSweep']['drainVoltageSetPoint'],
							gateVoltageMinimum=parameters['GateSweep']['gateVoltageMinimum'], 
							gateVoltageMaximum=parameters['GateSweep']['gateVoltageMaximum'], 
							stepsInVGSPerDirection=parameters['GateSweep']['stepsInVGSPerDirection'],
							pointsPerVGS=parameters['GateSweep']['pointsPerVGS'])
	smu_instance.rampDownVoltages()

	# Copy parameters and add in the test results
	jsonData = dict(parameters)
	jsonData['Results'] = results
	
	print('On/Off ratio: {:.4f}'.format(results['onOffRatio']))
	print('On current: {:.4e}'.format(results['onCurrent']))
	print('Off current: {:.4e}'.format(results['offCurrent']))

	# Save results as a JSON object
	if(isSavingResults):
		dlu.saveJSON(dlu.getDeviceDirectory(parameters), parameters['GateSweep']['saveFileName'], jsonData)

	# Show plots to the user
	if(isPlottingResults):
		deviceHistoryScript.run(deviceHistoryParameters, showFigures=True)
		
	return jsonData

# === Data Collection ===
def runGateSweep(smu_instance, isFastSweep, isAlternatingSweep, pulsedMeasurementOnTime, pulsedMeasurementOffTime, drainVoltageSetPoint, gateVoltageMinimum, gateVoltageMaximum, stepsInVGSPerDirection, pointsPerVGS):
	vds_data = [[],[]]
	id_data = [[],[]]
	vgs_data = [[],[]]
	ig_data = [[],[]]
	timestamps = [[],[]]

	# Generate list of gate voltages to apply
	if(isAlternatingSweep):
		gateVoltages = dgu.alternatingSweepValuesWithDuplicates(gateVoltageMaximum, stepsInVGSPerDirection*2*pointsPerVGS, pointsPerVGS)
	else:
		gateVoltages = dgu.sweepValuesWithDuplicates(gateVoltageMinimum, gateVoltageMaximum, stepsInVGSPerDirection*2*pointsPerVGS, pointsPerVGS)
		
		# Ramp gate and wait a few seconds for everything to settle down
		smu_instance.rampGateVoltageTo(gateVoltageMinimum, steps=20)
		time.sleep(1)

	if(isFastSweep):
		# Use SMU built-in sweep to sweep the gate forwards and backwards
		forward_measurements = smu_instance.takeSweep(drainVoltageSetPoint, drainVoltageSetPoint, gateVoltageMinimum, gateVoltageMaximum, stepsInVGSPerDirection)
		timestamps[0].append(time.time())
		reverse_measurements = smu_instance.takeSweep(drainVoltageSetPoint, drainVoltageSetPoint, gateVoltageMaximum, gateVoltageMinimum, stepsInVGSPerDirection)
		timestamps[1].append(time.time())

		# Save forward measurements
		vds_data[0] = forward_measurements['Vds_data']
		id_data[0]  = forward_measurements['Id_data']
		vgs_data[0] = forward_measurements['Vgs_data']
		ig_data[0]  = forward_measurements['Ig_data']

		# Save reverse measurements
		vds_data[1] = reverse_measurements['Vds_data']
		id_data[1]  = reverse_measurements['Id_data']
		vgs_data[1] = reverse_measurements['Vgs_data']
		ig_data[1]  = reverse_measurements['Ig_data']

		# Save true measured Vgs as the applied voltages
		gateVoltages = vgs_data
	else:
		for direction in [0,1]:
			for gateVoltage in gateVoltages[direction]:
				# Apply V_GS
				smu_instance.setVgs(gateVoltage)

				# If pulsedMeasurementOnTime is non-zero, hold the gate at Vgs for specified amount of time
				if(pulsedMeasurementOnTime > 0):
					time.sleep(pulsedMeasurementOnTime*0.9)

				# Take Measurement and save it
				measurement = smu_instance.takeMeasurement()

				if(pulsedMeasurementOnTime > 0):
					time.sleep(pulsedMeasurementOnTime*0.1)

				timestamp = time.time()
				
				vds_data[direction].append(measurement['V_ds'])
				id_data[direction].append(measurement['I_d'])
				vgs_data[direction].append(measurement['V_gs'])
				ig_data[direction].append(measurement['I_g'])
				timestamps[direction].append(timestamp)

				# If pulsedMeasurementOffTime is non-zero, ground the gate for specified amount of time, then bring it back
				if(pulsedMeasurementOffTime > 0):
					smu_instance.setVgs(0)
					time.sleep(pulsedMeasurementOffTime)

	return {
		'vds_data':vds_data,
		'id_data':id_data,
		'vgs_data':vgs_data,
		'ig_data':ig_data,
		'timestamps':timestamps,
		'gateVoltages':gateVoltages,
		'onOffRatio':onOffRatio(id_data),
		'onCurrent':onCurrent(id_data),
		'offCurrent':offCurrent(id_data)
	}

def onOffRatio(drainCurrent):
	return onCurrent(drainCurrent)/offCurrent(drainCurrent)

def onCurrent(drainCurrent):
	absDrainCurrent = abs(np.array(drainCurrent))
	return np.percentile(absDrainCurrent, 99)

def offCurrent(drainCurrent):
	absDrainCurrent = abs(np.array(drainCurrent))
	return (np.percentile(absDrainCurrent, 5))

	