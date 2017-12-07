import time
import sys

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

def run(parameters):
	smu_instance = smu.getConnectionFromVisa(parameters['NPLC'], parameters['complianceCurrent'])

	smu_instance.rampGateVoltage(0, parameters['gateVoltageSetPoint'], 20)
	smu_instance.rampDrainVoltage(0, parameters['drainVoltageSetPoint'], 20)
	
	progressBarLength = 70
	print('')
	for i in range(progressBarLength):
		time.sleep(parameters['time']/progressBarLength)
		print('\r[' + i*'=' + (progressBarLength-i-1)*' ' + ']', end='')

	print('')
	smu_instance.rampDownVoltages()


if __name__ == '__main__':
    run(default_parameters)