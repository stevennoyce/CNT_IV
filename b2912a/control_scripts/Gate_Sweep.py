import time
import numpy as np

from utilities import DataLoggerUtility as dlu
from utilities import DataGeneratorUtility as dgu
from utilities import DataPlotterUtility as dpu
from framework import SourceMeasureUnit as smu



# === Main ===
def run(parameters, smu_instance, isSavingResults=True, isPlottingResults=True):
	smu_instance.setComplianceCurrent(parameters['GateSweep']['complianceCurrent'])	

	# RUN TEST
	smu_instance.rampDrainVoltageTo(parameters['GateSweep']['drainVoltageSetPoint'])
	results = runGateSweep( smu_instance, 
							parameters['deviceDirectory'], 
							parameters['GateSweep']['saveFileName'], 
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
	
	# Display key metrics to the user
	print('On/Off ratio: {:.4f}'.format(results['onOffRatio']))
	print('On current: {:.4e}'.format(results['onCurrent']))
	print('Off current: {:.4e}'.format(results['offCurrent']))

	# Save results as a JSON object
	if(isSavingResults):
		dlu.saveJSON(parameters['deviceDirectory'], parameters['GateSweep']['saveFileName'], jsonData)

	# Show plots to the user
	if(isPlottingResults):
		dpu.plotJSON(jsonData, parameters, 'b')
		dpu.show()
		
	return jsonData


def runGateSweep(smu_instance, workingDirectory, saveFileName, isFastSweep, isAlternatingSweep, pulsedMeasurementOnTime, pulsedMeasurementOffTime, drainVoltageSetPoint, gateVoltageMinimum, gateVoltageMaximum, stepsInVGSPerDirection, pointsPerVGS):
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

	