import time
import numpy as np

from utilities import DataLoggerUtility as dlu
from utilities import DataGeneratorUtility as dgu
from utilities import DataPlotterUtility as dpu
from framework import SourceMeasureUnit as smu



# ## ********** Parameters **********

# chipID = 'C127-'
# deviceID = '0-0'

# #saveFolder = '/Users/stevennoyce/Documents/home/Research/illumina/PSoC/Layout 2_14/Version 2/Host/Testing/'
# saveFolder = '/Users/jaydoherty/Documents/myWorkspaces/Python/Research/CNT_IV/b2912a/data/'
# saveFileName = 'GateSweep_' + chipID

# default_parameters = {
# 	'runType':'GateSweep',
# 	'chipID':chipID,
# 	'deviceID':deviceID,
# 	'saveFolder':saveFolder,
# 	'saveFileName':saveFileName,
# 	'NPLC':1,
# 	'runDataPoints':600,
# 	'complianceCurrent':	50e-6,
# 	'drainVoltageSetPoint':	0.5,
# 	'gateVoltageMinimum':	-15.0,
# 	'gateVoltageMaximum':	15.0
# }



## ********** Main **********

def run(parameters, smu_instance, isSavingResults=True, isPlottingResults=True):
	smu_instance.setComplianceCurrent(parameters['GateSweep']['complianceCurrent'])	

	smu_instance.rampDrainVoltageTo(parameters['GateSweep']['drainVoltageSetPoint'], smu_instance.measurementsPerSecond/2)
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

	jsonData = {**parameters, **results}
	
	print('On/Off ratio: {:.4f}'.format(results['onOffRatio']))
	print('On current: {:.4e}'.format(results['onCurrent']))
	print('Off current: {:.4e}'.format(results['offCurrent']))

	if(isSavingResults):
		dlu.saveJSON(parameters['deviceDirectory'], parameters['GateSweep']['saveFileName'], jsonData)

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
				# Apply Vgs
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
		'voltage1s':vds_data,
		'current1s':id_data,
		'voltage2s':vgs_data,
		'current2s':ig_data,
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

	

if __name__ == '__main__':
    run(default_parameters)