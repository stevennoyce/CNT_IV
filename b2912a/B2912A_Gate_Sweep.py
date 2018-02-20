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
	dlu.makeFolder(parameters['deviceDirectory'])
	dlu.initCSV(parameters['deviceDirectory'], parameters['GateSweep']['saveFileName'])
	smu_instance.setComplianceCurrent(parameters['GateSweep']['complianceCurrent'])	

	smu_instance.rampDrainVoltageTo(parameters['GateSweep']['drainVoltageSetPoint'], 20)
	results = runGateSweep( smu_instance, 
							parameters['deviceDirectory'], 
							parameters['GateSweep']['saveFileName'], 
							isFastSweep=parameters['GateSweep']['runFastSweep'],
							drainVoltageSetPoint=parameters['GateSweep']['drainVoltageSetPoint'],
							gateVoltageMinimum=parameters['GateSweep']['gateVoltageMinimum'], 
							gateVoltageMaximum=parameters['GateSweep']['gateVoltageMaximum'], 
							points=parameters['GateSweep']['runDataPoints'],
							pointsPerVGS=parameters['GateSweep']['pointsPerVGS'],
							NPLC=parameters['NPLC'])
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


def runGateSweep(smu_instance, workingDirectory, saveFileName, isFastSweep, drainVoltageSetPoint, gateVoltageMinimum, gateVoltageMaximum, points, pointsPerVGS,  NPLC):
	vds_data = [[],[]]
	id_data = [[],[]]
	vgs_data = [[],[]]
	ig_data = [[],[]]
	timestamps = [[],[]]

	smu_instance.rampGateVoltage(0, gateVoltageMinimum, 20)
	gateVoltages = dgu.sweepValuesWithDuplicates(gateVoltageMinimum, gateVoltageMaximum, points, pointsPerVGS)
	
	if(isFastSweep):
		forward_measurements = smu_instance.takeSweep(drainVoltageSetPoint, drainVoltageSetPoint, gateVoltageMinimum, gateVoltageMaximum, points/2, NPLC)
		timestamps[0].append(time.time())
		reverse_measurements = smu_instance.takeSweep(drainVoltageSetPoint, drainVoltageSetPoint, gateVoltageMaximum, gateVoltageMinimum, points/2, NPLC)
		timestamps[1].append(time.time())

		vds_data[0] = forward_measurements['Vds_data']
		id_data[0]  = forward_measurements['Id_data']
		vgs_data[0] = forward_measurements['Vgs_data']
		ig_data[0]  = forward_measurements['Ig_data']

		vds_data[1] = reverse_measurements['Vds_data']
		id_data[1]  = reverse_measurements['Id_data']
		vgs_data[1] = reverse_measurements['Vgs_data']
		ig_data[1]  = reverse_measurements['Ig_data']

		gateVoltages = vgs_data
	else:
		for i in [0,1]:
			for gateVoltage in gateVoltages[i]:
				smu_instance.setVgs(gateVoltage)
				measurement = smu_instance.takeMeasurement()
				
				v_ds = measurement['V_ds']
				i_d  = measurement['I_d']
				v_gs = measurement['V_gs']
				i_g  = measurement['I_g']
				timestamp = time.time()

				csvData = [timestamp, v_ds, i_d, v_gs, i_g]
				dlu.saveCSV(workingDirectory, saveFileName, csvData)
				
				vds_data[i].append(v_ds)
				id_data[i].append(i_d)
				vgs_data[i].append(v_gs)
				ig_data[i].append(i_g)
				timestamps[i].append(timestamp)

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