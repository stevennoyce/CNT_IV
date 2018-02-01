import time
import numpy as np

from utilities import DataLoggerUtility as dlu
from utilities import DataPlotterUtility as dpu
from framework import SourceMeasureUnit as smu

# ## ********** Parameters **********

# default_parameters = {
# 	'runType':'StaticBias',
# 	'chipID':'C127-',
# 	'deviceID':'0-0',
# 	'NPLC':1,
# 	'time': 30,
# 	'complianceCurrent':	100e-6,
# 	'gateVoltageSetPoint':	-15.0,
# 	'drainVoltageSetPoint':	0.5,
# }

def run(parameters, smu_instance, isSavingResults=True, isPlottingResults=True):
	print('Applying static bias of V_GS='+str(parameters['gateVoltageSetPoint'])+'V, V_DS='+str(parameters['drainVoltageSetPoint'])+'V for '+str(parameters['biasTime'])+' seconds...')

	dlu.makeFolder(parameters['deviceDirectory'])
	smu_instance.setComplianceCurrent(parameters['StaticBias']['complianceCurrent'])	

	smu_instance.rampGateVoltageTo(parameters['StaticBias']['gateVoltageSetPoint'], steps=30)
	smu_instance.rampDrainVoltageTo(parameters['StaticBias']['drainVoltageSetPoint'], steps=30)

	results = runStaticBias(smu_instance, 
							parameters['NPLC'],
							parameters['StaticBias']['drainVoltageSetPoint'],
							parameters['StaticBias']['gateVoltageSetPoint'],
							parameters['StaticBias']['startUpSettlingDelay'],
							parameters['StaticBias']['biasTime'], 
							parameters['StaticBias']['runDataPoints'])

	if(parameters['StaticBias']['groundGateWhenDone']):
		smu_instance.rampGateVoltageDown(steps=40)
	if(parameters['StaticBias']['groundDrainWhenDone']):
		smu_instance.rampDrainVoltageDown(steps=40)

	jsonData = {**parameters, **results}
	
	if(isSavingResults):
		dlu.saveJSON(parameters['deviceDirectory'], parameters['StaticBias']['saveFileName'], jsonData)

	if(isPlottingResults):
		dpu.plotJSON(jsonData, parameters, 'b')
		dpu.show()

	return jsonData

def runStaticBias(smu_instance, NPLC, drainVoltageSetPoint, gateVoltageSetPoint, startUpDelay, biasTime, steps):
	voltage1s = []
	current1s = []
	voltage2s = []
	current2s = []
	timestamps = []

	if(startUpDelay > 0):
		time.sleep(startUpDelay)

	for i in range(steps):
		timeBetweenMeasurements = float(biasTime)/steps
		measurements = smu_instance.takeSweep(drainVoltageSetPoint, drainVoltageSetPoint, gateVoltageSetPoint, gateVoltageSetPoint, timeBetweenMeasurements*60/1.5, NPLC)
		timestamp = time.time()
		
		voltage1s.append(np.mean(measurements['voltage1s']))
		current1s.append(np.mean(measurements['current1s']))
		voltage2s.append(np.mean(measurements['voltage2s']))
		current2s.append(np.mean(measurements['current2s']))
		timestamps.append(timestamp)

		print('\r[' + int(i*70.0/steps)*'=' + (70-int(i*70.0/steps)-1)*' ' + ']', end='')
	print('')

	return {
		'voltage1s':voltage1s,
		'current1s':current1s,
		'voltage2s':voltage2s,
		'current2s':current2s,
		'timestamps':timestamps
	}



if __name__ == '__main__':
    run(default_parameters)