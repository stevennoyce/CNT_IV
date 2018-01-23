import time

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

def run(parameters, isSavingResults=True, isPlottingResults=True):
	workingDirectory = parameters['saveFolder'] + parameters['chipID'] + '/' + parameters['deviceID'] + '/'
	dlu.makeFolder(workingDirectory)

	print('Applying static bias of V_GS='+str(parameters['gateVoltageSetPoint'])+'V, V_DS='+str(parameters['drainVoltageSetPoint'])+'V for '+str(parameters['biasTime'])+' seconds...')
	smu_instance = smu.getConnectionFromVisa(parameters['NPLC'], parameters['complianceCurrent'])

	smu_instance.rampGateVoltage(0, parameters['gateVoltageSetPoint'], 30)
	smu_instance.rampDrainVoltage(0, parameters['drainVoltageSetPoint'], 30)

	results = runStaticBias(smu_instance, 
							parameters['startUpSettlingDelay'],
							parameters['biasTime'], 
							parameters['runDataPoints'])
	smu_instance.rampDownVoltages()

	jsonData = {**parameters, **results}
	
	if(isSavingResults):
		dlu.saveJSON(workingDirectory, parameters['saveFileName'], jsonData)

	if(isPlottingResults):
		dpu.plotJSON(jsonData, 'b')
		dpu.show()

	return jsonData

def runStaticBias(smu_instance, startUpDelay, biasTime, steps):
	voltage1s = []
	current1s = []
	voltage2s = []
	current2s = []
	timestamps = []

	time.sleep(startUpDelay)

	for i in range(steps):
		time.sleep(float(biasTime)/steps)

		measurement = smu_instance.takeMeasurement()
		timestamp = time.time()
		
		voltage1s.append(measurement[0])
		current1s.append(measurement[1])
		voltage2s.append(measurement[6])
		current2s.append(measurement[7])
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